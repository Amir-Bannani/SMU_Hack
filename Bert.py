"""
Simplified BERT Report Difficulty Analyzer
No Trainer required - uses plain PyTorch
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
import numpy as np
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


class ReportDataset(Dataset):
    """Custom dataset for reports"""
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


class DifficultyAnalyzer:
    def __init__(self, model_name='distilbert-base-uncased', num_labels=11):
        """Initialize with DistilBERT (lighter than BERT)"""
        print(f"Loading {model_name}...")
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model = DistilBertForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels
        )
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        print(f"Model loaded on {self.device}")
    
    def train(self, train_texts, train_labels, val_texts=None, val_labels=None,
              epochs=3, batch_size=8, learning_rate=2e-5):
        """Train the model with simple PyTorch loop"""
        
        # Create datasets
        train_dataset = ReportDataset(train_texts, train_labels, self.tokenizer)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        val_loader = None
        if val_texts is not None:
            val_dataset = ReportDataset(val_texts, val_labels, self.tokenizer)
            val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        # Optimizer and loss
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=learning_rate)
        criterion = nn.CrossEntropyLoss()
        
        # Training loop
        for epoch in range(epochs):
            print(f"\n{'='*60}")
            print(f"Epoch {epoch + 1}/{epochs}")
            print('='*60)
            
            # Training phase
            self.model.train()
            total_loss = 0
            predictions, true_labels = [], []
            
            progress_bar = tqdm(train_loader, desc="Training")
            for batch in progress_bar:
                # Move to device
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                
                # Forward pass
                optimizer.zero_grad()
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                total_loss += loss.item()
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                # Track predictions
                preds = torch.argmax(outputs.logits, dim=1)
                predictions.extend(preds.cpu().numpy())
                true_labels.extend(labels.cpu().numpy())
                
                progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})
            
            # Calculate metrics
            avg_loss = total_loss / len(train_loader)
            accuracy = accuracy_score(true_labels, predictions)
            mae = mean_absolute_error(true_labels, predictions)
            
            print(f"\nTraining Loss: {avg_loss:.4f}")
            print(f"Training Accuracy: {accuracy:.4f}")
            print(f"Training MAE: {mae:.4f}")
            
            # Validation phase
            if val_loader:
                val_loss, val_acc, val_mae = self._evaluate(val_loader, criterion)
                print(f"\nValidation Loss: {val_loss:.4f}")
                print(f"Validation Accuracy: {val_acc:.4f}")
                print(f"Validation MAE: {val_mae:.4f}")
        
        print("\n✓ Training completed!")
    
    def _evaluate(self, dataloader, criterion):
        """Evaluate on validation set"""
        self.model.eval()
        total_loss = 0
        predictions, true_labels = [], []
        
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Validating"):
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                total_loss += loss.item()
                
                preds = torch.argmax(outputs.logits, dim=1)
                predictions.extend(preds.cpu().numpy())
                true_labels.extend(labels.cpu().numpy())
        
        avg_loss = total_loss / len(dataloader)
        accuracy = accuracy_score(true_labels, predictions)
        mae = mean_absolute_error(true_labels, predictions)
        
        return avg_loss, accuracy, mae
    
    def predict(self, texts):
        """Predict difficulty scores"""
        self.model.eval()
        
        dataset = ReportDataset(texts, [0]*len(texts), self.tokenizer)
        dataloader = DataLoader(dataset, batch_size=8)
        
        all_predictions = []
        all_probabilities = []
        
        with torch.no_grad():
            for batch in dataloader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                )
                
                probs = torch.softmax(outputs.logits, dim=1)
                preds = torch.argmax(probs, dim=1)
                
                all_predictions.extend(preds.cpu().numpy())
                all_probabilities.extend(probs.cpu().numpy())
        
        return np.array(all_predictions), np.array(all_probabilities)
    
    def predict_with_confidence(self, texts):
        """Predict with confidence scores"""
        predictions, probabilities = self.predict(texts)
        confidence = np.max(probabilities, axis=1)
        return predictions, confidence
    
    def save_model(self, path='./difficulty_model'):
        """Save model and tokenizer"""
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        print(f"✓ Model saved to {path}")
    
    def load_model(self, path='./difficulty_model'):
        """Load saved model"""
        self.model = DistilBertForSequenceClassification.from_pretrained(path)
        self.tokenizer = DistilBertTokenizer.from_pretrained(path)
        self.model.to(self.device)
        print(f"✓ Model loaded from {path}")


def create_sample_data():
    """Create sample training data - expanded dataset"""
    reports = [
        # Score 0-2: No issues (10 examples)
        "This week went perfectly. All tasks completed ahead of schedule.",
        "Great progress on all fronts. Team working efficiently together.",
        "No blockers encountered. Everything proceeding as planned.",
        "Smooth week with excellent results. All milestones achieved.",
        "Tasks completed successfully. No difficulties to report.",
        "Outstanding week. Exceeded all expectations and delivered early.",
        "Perfect execution. All deliverables completed without issues.",
        "Excellent collaboration. Everything running smoothly.",
        "All objectives met. No problems encountered this week.",
        "Flawless week. Project progressing better than expected.",
        
        # Score 3-5: Minor issues (10 examples)
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
        
        # Score 6-8: Significant problems (10 examples)
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
        
        # Score 9-10: Critical (10 examples)
        "Critical production bug. System completely down. All hands needed.",
        "Completely blocked by missing dependencies. Cannot proceed at all.",
        "Severe technical debt causing project to halt. Immediate action required.",
        "Client escalated major issues. Project timeline at serious risk.",
        "Infrastructure failure. Lost significant work. Emergency situation.",
        "Data breach detected. Emergency response team activated immediately.",
        "Complete system failure. Revenue impact. CEO involved.",
        "Showstopper bug found day before release. Launch must be delayed.",
        "Critical resource left company. Knowledge transfer incomplete. Crisis mode.",
        "Legal compliance issue discovered. Project may need complete restart."
    ]
    
    labels = [
        1, 0, 1, 0, 1, 0, 1, 0, 2, 1,  # 0-2: 10 examples
        4, 3, 4, 3, 5, 4, 3, 4, 5, 3,  # 3-5: 10 examples
        7, 8, 6, 7, 6, 8, 7, 6, 8, 7,  # 6-8: 10 examples
        10, 9, 9, 10, 9, 10, 9, 10, 9, 10  # 9-10: 10 examples
    ]
    
    return reports, labels


def interpret_score(score):
    """Human-readable interpretation"""
    if score <= 2:
        return "✓ No significant difficulties"
    elif score <= 5:
        return "⚠ Minor issues, manageable"
    elif score <= 8:
        return "⚠⚠ Significant problems, attention needed"
    else:
        return "🚨 CRITICAL - Immediate action required"


def main():
    """Main training and testing pipeline"""
    
    # Create sample data
    print("Preparing sample data...")
    reports, labels = create_sample_data()
    
    # Split data (remove stratify for small datasets)
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        reports, labels, test_size=0.2, random_state=42
    )
    
    print(f"Training samples: {len(train_texts)}")
    print(f"Validation samples: {len(val_texts)}")
    
    # Initialize and train
    analyzer = DifficultyAnalyzer()
    
    analyzer.train(
        train_texts=train_texts,
        train_labels=train_labels,
        val_texts=val_texts,
        val_labels=val_labels,
        epochs=3,
        batch_size=4,
        learning_rate=2e-5
    )
    
    # Test predictions
    print("\n" + "="*60)
    print("Testing on New Reports")
    print("="*60)
    
    test_reports = [
        "Everything going smoothly. All deliverables on time.",
        "Having some difficulty with the new framework. Need some guidance.",
        "Critical production issue. System completely offline. Emergency!",
        "Minor bug found but already have a fix ready to deploy."
    ]
    
    predictions, confidence = analyzer.predict_with_confidence(test_reports)
    
    for i, report in enumerate(test_reports):
        print(f"\n📝 Report: {report}")
        print(f"   Difficulty Score: {predictions[i]}/10")
        print(f"   Confidence: {confidence[i]:.1%}")
        print(f"   Status: {interpret_score(predictions[i])}")
    
    # Save model
    analyzer.save_model()


if __name__ == "__main__":
    print("="*60)
    print("Employee Report Difficulty Analyzer")
    print("Using DistilBERT (lighter & faster than BERT)")
    print("="*60)
    main()