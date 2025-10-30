"""
Money Flow Classifier - ML Model for predicting money flow direction.

This model predicts whether money will flow in (buy pressure) or out (sell pressure)
based on historical price, volume, and indicator patterns.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict
import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler

from utils.logger import get_logger
from utils.config import get_config
from ml_models.feature_engineering import FeatureEngineering

logger = get_logger('ml_models')


class MoneyFlowClassifier:
    """
    ML model for predicting money flow direction.
    
    Uses RandomForest and GradientBoosting ensemble.
    """
    
    def __init__(self, model_type: str = 'random_forest'):
        """
        Initialize Money Flow Classifier.
        
        Args:
            model_type: Type of model ('random_forest' or 'gradient_boosting')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
        # Get model parameters from config
        config = get_config()
        params = config.get_ml_params('money_flow_classifier')
        
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=params.get('n_estimators', 100),
                max_depth=params.get('max_depth', 10),
                min_samples_split=params.get('min_samples_split', 5),
                min_samples_leaf=params.get('min_samples_leaf', 2),
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=params.get('n_estimators', 100),
                max_depth=params.get('max_depth', 5),
                learning_rate=params.get('learning_rate', 0.1),
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        logger.info(f"✅ Money Flow Classifier initialized ({model_type})")
    
    def prepare_data(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Prepare data for training.
        
        Args:
            df: DataFrame with features and target
            test_size: Proportion of data for testing
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Engineer features if not already done
        fe = FeatureEngineering()
        if 'target' not in df.columns:
            df = fe.engineer_all_features(df, include_indicators=True)
        
        # Prepare ML data
        X, y = fe.prepare_ml_data(df, drop_na=True)
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrame
        X_train = pd.DataFrame(X_train_scaled, columns=self.feature_names)
        X_test = pd.DataFrame(X_test_scaled, columns=self.feature_names)
        
        logger.info(f"📊 Data prepared: {len(X_train)} train, {len(X_test)} test samples")
        
        return X_train, X_test, y_train, y_test
    
    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        cv_folds: int = 5
    ) -> Dict:
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training target
            cv_folds: Number of cross-validation folds
            
        Returns:
            Dictionary with training metrics
        """
        logger.info(f"🎓 Training {self.model_type} model...")
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train, y_train,
            cv=cv_folds, scoring='roc_auc'
        )
        
        # Training metrics
        train_pred = self.model.predict(X_train)
        train_proba = self.model.predict_proba(X_train)[:, 1]
        
        metrics = {
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'train_accuracy': (train_pred == y_train).mean(),
            'train_roc_auc': roc_auc_score(y_train, train_proba)
        }
        
        self.is_trained = True
        
        logger.info(f"✅ Training completed!")
        logger.info(f"   CV ROC-AUC: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
        logger.info(f"   Train accuracy: {metrics['train_accuracy']:.4f}")
        
        return metrics
    
    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict:
        """
        Evaluate the model on test data.
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        logger.info("📊 Evaluating model...")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Metrics
        accuracy = (y_pred == y_test).mean()
        roc_auc = roc_auc_score(y_test, y_proba)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        metrics = {
            'accuracy': accuracy,
            'roc_auc': roc_auc,
            'precision': report['1']['precision'],
            'recall': report['1']['recall'],
            'f1_score': report['1']['f1-score'],
            'confusion_matrix': cm
        }
        
        logger.info(f"✅ Evaluation completed!")
        logger.info(f"   Test accuracy: {accuracy:.4f}")
        logger.info(f"   ROC-AUC: {roc_auc:.4f}")
        logger.info(f"   Precision: {metrics['precision']:.4f}")
        logger.info(f"   Recall: {metrics['recall']:.4f}")
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features DataFrame
            
        Returns:
            Array of predictions (0 or 1)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict probabilities.
        
        Args:
            X: Features DataFrame
            
        Returns:
            Array of probabilities for class 1
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict_proba(X_scaled)[:, 1]
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance.
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        importance = self.model.feature_importances_
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return importance_df.head(top_n)
    
    def save(self, path: str):
        """
        Save model to disk.
        
        Args:
            path: Path to save model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_type': self.model_type
        }
        
        joblib.dump(model_data, save_path)
        logger.info(f"💾 Model saved to {save_path}")
    
    def load(self, path: str):
        """
        Load model from disk.
        
        Args:
            path: Path to load model from
        """
        model_data = joblib.load(path)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.model_type = model_data['model_type']
        self.is_trained = True
        
        logger.info(f"📂 Model loaded from {path}")


if __name__ == '__main__':
    """Test Money Flow Classifier."""
    print("=" * 70)
    print("🤖 Testing Money Flow Classifier")
    print("=" * 70)
    
    from data_collection.binance_client import BinanceClient
    
    # Fetch historical data
    print("\n📈 Fetching historical BTC data...")
    client = BinanceClient()
    df = client.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=1000)
    
    print(f"✅ Fetched {len(df)} candles")
    
    # Initialize classifier
    print("\n🤖 Initializing Money Flow Classifier...")
    classifier = MoneyFlowClassifier(model_type='random_forest')
    
    # Prepare data
    print("\n📊 Preparing data...")
    X_train, X_test, y_train, y_test = classifier.prepare_data(df, test_size=0.2)
    
    print(f"   Train samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    print(f"   Features: {len(classifier.feature_names)}")
    print(f"   Target distribution (train): {y_train.sum()} positive ({y_train.sum()/len(y_train)*100:.1f}%)")
    
    # Train model
    print("\n🎓 Training model...")
    train_metrics = classifier.train(X_train, y_train, cv_folds=5)
    
    print(f"\n✅ Training metrics:")
    print(f"   CV ROC-AUC: {train_metrics['cv_mean']:.4f} (+/- {train_metrics['cv_std']:.4f})")
    print(f"   Train accuracy: {train_metrics['train_accuracy']:.4f}")
    
    # Evaluate model
    print("\n📊 Evaluating model...")
    eval_metrics = classifier.evaluate(X_test, y_test)
    
    print(f"\n✅ Test metrics:")
    print(f"   Accuracy: {eval_metrics['accuracy']:.4f}")
    print(f"   ROC-AUC: {eval_metrics['roc_auc']:.4f}")
    print(f"   Precision: {eval_metrics['precision']:.4f}")
    print(f"   Recall: {eval_metrics['recall']:.4f}")
    print(f"   F1-Score: {eval_metrics['f1_score']:.4f}")
    
    print(f"\n📊 Confusion Matrix:")
    print(eval_metrics['confusion_matrix'])
    
    # Feature importance
    print("\n📊 Top 10 Most Important Features:")
    importance = classifier.get_feature_importance(top_n=10)
    for idx, row in importance.iterrows():
        print(f"   {row['feature']:<25} {row['importance']:.4f}")
    
    # Test prediction on latest data
    print("\n🔮 Testing prediction on latest data...")
    latest_features = X_test.tail(5)
    predictions = classifier.predict(latest_features)
    probabilities = classifier.predict_proba(latest_features)
    
    print("\n📊 Latest predictions:")
    for i, (pred, proba) in enumerate(zip(predictions, probabilities)):
        signal = "BUY" if pred == 1 else "HOLD"
        print(f"   Sample {i+1}: {signal} (probability: {proba:.2%})")
    
    # Save model
    print("\n💾 Saving model...")
    classifier.save('models/money_flow_classifier.pkl')
    print("   Model saved successfully!")
    
    print("\n" + "=" * 70)
    print("🎉 Money Flow Classifier test completed successfully!")
    print("=" * 70)
