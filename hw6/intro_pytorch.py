import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms



def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """

    
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    train_set=datasets.FashionMNIST('./data',train=True, download=True,transform=transform)
    test_set=datasets.FashionMNIST('./data', train=False, transform=transform)

    loader = torch.utils.data.DataLoader(train_set if training == True else test_set, batch_size = 64)
    return loader

def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10)
            )
    return model



def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(T):
        correct = 0
        total = 0
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            opt.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()

            running_loss += loss.item()
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct += 1
                total += 1

        avg_loss = running_loss / len(train_loader)
        accuracy = 100. * correct / total
        print(f"Train Epoch: {epoch} Accuracy: {correct}/{total}({accuracy:.2f}%) Loss: {avg_loss:.3f}")
        


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    correct = 0
    total = 0
    running_loss = 0.0
    with torch.no_grad():
        for i, data in enumerate(test_loader, 0):
            inputs, labels = data
            outputs = model(inputs)
            running_loss += criterion(outputs, labels).item()
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct += 1
                total += 1
    avg_loss = running_loss / len(test_loader)
    accuracy = correct/total
    if (show_loss):
        print(f"Average loss: {avg_loss:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt'
                   ,'Sneaker','Bag','Ankle Boot']
    img = test_images[index]
    outputs = model(img)
    prob = F.softmax(outputs, dim=1)
    top3_probs, top3_indices = torch.topk(prob, 3)
    for i in range(3):
        print(f"{class_names[top3_indices[0][i]]}: {top3_probs[0][i].item():.2f}%")




if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    train_loader = get_data_loader()
    print(type(train_loader))
    print(train_loader.dataset)
    test_loader = get_data_loader(False)
    # dataiter = iter(train_loader)
    # images, labels = dataiter.__next__()
    # print(images.shape)
    model = build_model()
    print(model)

    criterion = nn.CrossEntropyLoss()
    train_model(model, train_loader, criterion, 5)
    evaluate_model(model, test_loader, criterion, show_loss = False)
    evaluate_model(model, test_loader, criterion, show_loss = True)
    dataiter = iter(train_loader)
    images, labels = dataiter.__next__()
    predict_label(model, images, 1)
