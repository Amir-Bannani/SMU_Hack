"""
Employee Report Difficulty Analyzer
Uses Sentence-BERT + XGBoost - MUCH better for small datasets!
"""

from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')


class DifficultyAnalyzer:
    """Lightweight analyzer that works well with small datasets"""
    
    def __init__(self, model_type='gradient_boosting'):
        """
        Initialize analyzer
        model_type: 'logistic', 'svm', 'random_forest', 'gradient_boosting'
        """
        print("Loading Sentence-BERT model...")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Choose classifier
        self.model_type = model_type
        if model_type == 'logistic':
            self.classifier = LogisticRegression(max_iter=1000, random_state=42)
        elif model_type == 'svm':
            self.classifier = SVC(kernel='rbf', probability=True, random_state=42)
        elif model_type == 'random_forest':
            self.classifier = RandomForestClassifier(
                n_estimators=100, 
                max_depth=10,
                random_state=42
            )
        else:  # gradient_boosting (best for this task)
            self.classifier = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        
        print(f"✓ Using {model_type} classifier")
    
    def train(self, train_texts, train_labels, val_texts=None, val_labels=None):
        """Train the model"""
        print("\n" + "="*60)
        print("Training Phase")
        print("="*60)
        
        # Get embeddings
        print("Encoding training texts...")
        train_embeddings = self.encoder.encode(train_texts, show_progress_bar=True)
        
        # Cross-validation score
        print("\nPerforming cross-validation...")
        cv_scores = cross_val_score(
            self.classifier, 
            train_embeddings, 
            train_labels, 
            cv=min(5, len(train_texts)//2),
            scoring='accuracy'
        )
        print(f"CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        # Train
        print("Training classifier...")
        self.classifier.fit(train_embeddings, train_labels)
        
        # Training accuracy
        train_preds = self.classifier.predict(train_embeddings)
        train_acc = accuracy_score(train_labels, train_preds)
        train_mae = mean_absolute_error(train_labels, train_preds)
        
        print(f"\nTraining Results:")
        print(f"  Accuracy: {train_acc:.3f}")
        print(f"  MAE: {train_mae:.3f}")
        
        # Validation
        if val_texts is not None and val_labels is not None:
            print("\n" + "="*60)
            print("Validation Phase")
            print("="*60)
            
            val_embeddings = self.encoder.encode(val_texts, show_progress_bar=True)
            val_preds = self.classifier.predict(val_embeddings)
            val_acc = accuracy_score(val_labels, val_preds)
            val_mae = mean_absolute_error(val_labels, val_preds)
            
            print(f"\nValidation Results:")
            print(f"  Accuracy: {val_acc:.3f}")
            print(f"  MAE: {val_mae:.3f}")
            
            # Show detailed report
            print("\nDetailed Classification Report:")
            print(classification_report(val_labels, val_preds, zero_division=0))
        
        print("\n✓ Training completed!")
    
    def predict(self, texts):
        """Predict difficulty scores"""
        embeddings = self.encoder.encode(texts, show_progress_bar=False)
        predictions = self.classifier.predict(embeddings)
        return predictions
    
    def predict_with_confidence(self, texts):
        """Predict with confidence scores"""
        embeddings = self.encoder.encode(texts, show_progress_bar=False)
        
        # Get predictions
        predictions = self.classifier.predict(embeddings)
        
        # Get probabilities (confidence)
        if hasattr(self.classifier, 'predict_proba'):
            probabilities = self.classifier.predict_proba(embeddings)
            confidence = np.max(probabilities, axis=1)
        else:
            confidence = np.ones(len(predictions))  # SVM without probability
        
        return predictions, confidence
    
    def save_model(self, path='difficulty_model.pkl'):
        """Save the trained model"""
        model_data = {
            'classifier': self.classifier,
            'model_type': self.model_type
        }
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"✓ Model saved to {path}")
    
    def load_model(self, path='difficulty_model.pkl'):
        """Load a trained model"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        self.classifier = model_data['classifier']
        self.model_type = model_data['model_type']
        print(f"✓ Model loaded from {path}")


def create_training_data():
    """Create comprehensive training dataset"""
    reports = [
        # Difficulty 0-2: No issues (15 examples)
        "This week went perfectly. All tasks completed ahead of schedule.",
        "Great progress on all fronts. Team working efficiently together.",
        "No blockers encountered. Everything proceeding as planned.",
        "Smooth week with excellent results. All milestones achieved.",
        "Tasks completed successfully. No difficulties to report.",
        "Outstanding week. Exceeded expectations and delivered early.",
        "Perfect execution. All deliverables completed without issues.",
        "Excellent collaboration. Everything running smoothly.",
        "All objectives met. No problems encountered this week.",
        "Flawless week. Project progressing better than expected.",
        "Very productive week. All sprint goals achieved.",
        "Team performing excellently. No issues whatsoever.",
        "Fantastic progress. Everything on track and on budget.",
        "Completed all tasks efficiently. No challenges faced.",
        "Seamless week. All systems operational and stable.",
        
        # Difficulty 3-5: Minor issues (15 examples)
        "Had some minor delays due to unclear requirements from client.",
        "Encountered small bugs but managed to resolve them independently.",
        "Waiting for feedback from stakeholder. Slight delay expected.",
        "Minor technical issues slowed progress but nothing critical.",
        "Some confusion about priorities. Need clarification from manager.",
        "Small setback with testing environment. Working on resolution.",
        "Dependency update caused minor issues. Fixed most of them.",
        "Communication gaps led to small delays. Nothing major.",
        "Minor documentation issues. Taking extra time to clarify.",
        "Slight scope creep detected. Need to realign with team.",
        "A few small bugs appeared but quickly resolved them.",
        "Had to redo some work due to minor misunderstanding.",
        "Waiting on approvals which caused slight delays.",
        "Minor compatibility issues but found workarounds.",
        "Small learning curve with new tool slowed me down a bit.",
        
        # Difficulty 6-8: Significant problems (15 examples)
        "Facing technical challenges with API integration. Need senior help.",
        "Database performance issues causing significant delays in testing.",
        "Struggling with complex algorithm. Behind schedule by 2 days.",
        "Third-party service outage impacting our development workflow.",
        "Team member sick. Workload increased. Having difficulty keeping up.",
        "Major bug discovered in core module. Requires significant refactoring.",
        "Integration tests failing repeatedly. Root cause still unclear.",
        "Client changed requirements mid-sprint. Significant rework needed.",
        "Performance bottleneck identified. Needs architectural changes.",
        "Security vulnerability found. Must address before deployment.",
        "Complex technical debt blocking progress. Need team discussion.",
        "Significant delays due to external dependency failures.",
        "Struggling with implementation. May need to redesign approach.",
        "Multiple bugs found in production. Firefighting mode activated.",
        "Infrastructure issues causing development environment problems.",
        
        # Difficulty 9-10: Critical (15 examples)
        "Critical production bug. System completely down. All hands needed.",
        "Completely blocked by missing dependencies. Cannot proceed at all.",
        "Severe technical debt causing project to halt. Immediate action required.",
        "Client escalated major issues. Project timeline at serious risk.",
        "Infrastructure failure. Lost significant work. Emergency situation.",
        "Data breach detected. Emergency response team activated immediately.",
        "Complete system failure. Revenue impact. CEO involved.",
        "Showstopper bug found day before release. Launch must be delayed.",
        "Critical resource left company. Knowledge transfer incomplete. Crisis mode.",
        "Legal compliance issue discovered. Project may need complete restart.",
        "Catastrophic failure. All services offline. Maximum priority.",
        "Security incident. Customer data at risk. Immediate escalation.",
        "Production database corrupted. Data recovery in progress. Critical.",
        "Total project failure. Client threatening contract termination.",
        "System hack detected. Full security audit required immediately.",
    ]
    
    labels = [
        # 0-2: 15 examples
        1, 0, 1, 0, 1, 0, 1, 0, 2, 1, 1, 0, 2, 1, 0,
        # 3-5: 15 examples
        4, 3, 4, 3, 5, 4, 3, 4, 5, 3, 4, 5, 3, 4, 5,
        # 6-8: 15 examples
        7, 8, 6, 7, 6, 8, 7, 6, 8, 7, 6, 7, 8, 7, 6,
        # 9-10: 15 examples
        10, 9, 9, 10, 9, 10, 9, 10, 9, 10, 10, 9, 10, 9, 10
    ]
    
    return reports, labels


def interpret_score(score):
    """Human-readable interpretation"""
    if score <= 2:
        return "✓ No significant difficulties"
    elif score <= 5:
        return "⚠️ Minor issues, manageable"
    elif score <= 8:
        return "⚠️⚠️ Significant problems, attention needed"
    else:
        return "🚨 CRITICAL - Immediate action required"


def main():
    """Main training and testing pipeline"""
    
    print("="*60)
    print("Employee Report Difficulty Analyzer")
    print("Using Sentence-BERT + Gradient Boosting")
    print("="*60)
    
    # Create training data
    print("\nPreparing training data...")
    reports, labels = create_training_data()
    print(f"Total samples: {len(reports)}")
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        reports, labels, test_size=0.25, random_state=42
    )
    
    print(f"Training samples: {len(train_texts)}")
    print(f"Validation samples: {len(val_texts)}")
    
    # Train model
    analyzer = DifficultyAnalyzer(model_type='gradient_boosting')
    analyzer.train(train_texts, train_labels, val_texts, val_labels)
    
    # Test on new reports
    print("\n" + "="*60)
    print("Testing on New Reports")
    print("="*60)
    
    test_reports = [
        "Everything going smoothly. All deliverables on time.",
        "Having some difficulty with the new framework. Need some guidance.",
        "Critical production issue. System completely offline. Emergency!",
        "Minor bug found but already have a fix ready to deploy.",
        "Major blocker. Cannot proceed without help from senior developer.",
        "Week went well. Small delay but caught up quickly."
    ]
    
    predictions, confidence = analyzer.predict_with_confidence(test_reports)
    
    for i, report in enumerate(test_reports):
        print(f"\n📝 Report: {report}")
        print(f"   Difficulty Score: {predictions[i]}/10")
        print(f"   Confidence: {confidence[i]:.1%}")
        print(f"   Status: {interpret_score(predictions[i])}")
    
    # Save model
    analyzer.save_model()
    
    print("\n" + "="*60)
    print("✓ Training Complete! Model saved successfully.")
    print("="*60)


if __name__ == "__main__":
    main()