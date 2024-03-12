from sklearn.metrics import accuracy_score, confusion_matrix, auc
import matplotlib.pyplot as plt


def calculate_non_correlated_features(X_train, threshold):
    correlation_matrix = X_train.corr()

    high_correlation_mask = (abs(correlation_matrix) >= threshold) & (correlation_matrix != 1.0)

    highly_correlated_columns = set()
    for col in correlation_matrix.columns:
        highly_correlated_columns.update(correlation_matrix.index[high_correlation_mask[col]])

    return [col for col in X_train.columns if col not in highly_correlated_columns]


def print_results(y_val, y_pred):
    accuracy = accuracy_score(y_val, y_pred)
    print("Accuracy:", accuracy)

    conf_matrix = confusion_matrix(y_val, y_pred)
    print("Confusion Matrix:")
    print(conf_matrix)

def plot_roc(fpr, tpr):
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.show()