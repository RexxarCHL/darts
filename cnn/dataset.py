

CIFAR_CLASSES = 10
MNIST_CLASSES = 10
FASHION_CLASSES = 10
EMNIST_CLASSES = 47
SVHN_CLASSES = 10
STL10_CLASSES = 10
DEVANAGARI_CLASSES = 46

class_dict = {'cifar10': CIFAR_CLASSES,
              'mnist' : MNIST_CLASSES,
              'emnist': EMNIST_CLASSES,
              'fashion': FASHION_CLASSES,
              'svhn': SVHN_CLASSES,
              'stl10': STL10_CLASSES,
              'devanagari' : DEVANAGARI_CLASSES}

inp_channel_dict = {'cifar10': 3,
                    'mnist' : 1,
                    'emnist': 1,
                    'fashion': 1,
                    'svhn': 3,
                    'stl10': 3,
                    'devanagari' : 1}

def get_training_queues(dataset_name, train_transform):
  print("Getting",args.dataset,"data")
  if args.dataset == 'cifar10':
    print("Using CIFAR10")
    train_data = dset.CIFAR10(root=dataset_name, train=True, download=True, transform=train_transform)
  elif args.dataset == 'mnist':
    print("Using MNIST")
    train_data = dset.MNIST(root=dataset_name, train=True, download=True, transform=train_transform)
  elif args.dataset == 'emnist':
    print("Using EMNIST")
    train_data = dset.EMNIST(root=dataset_name, split='balanced', train=True, download=True, transform=train_transform)
  elif args.dataset == 'fashion':
    print("Using Fashion")
    train_data = dset.FashionMNIST(root=dataset_name, train=True, download=True, transform=train_transform)
  elif args.dataset == 'svhn':
    print("Using SVHN")
    train_data = dset.SVHN(root=dataset_name, split='train', download=True, transform=train_transform)
  elif args.dataset == 'stl10':
    print("Using STL10")
    train_data = dset.STL10(root=dataset_name, split='train', download=True, transform=train_transform)
  elif args.dataset == 'devanagari':
    print("Using DEVANAGARI")
    def grey_pil_loader(path):
      # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
      with open(path, 'rb') as f:
          img = Image.open(f)
          img = img.convert('L')
          return img
    # Ensure dataset is present in the directory args.data. Does not support auto download
    train_data = dset.ImageFolder(root=args.data, transform=train_transform, loader = grey_pil_loader)
  else:
    assert False, "Cannot get training queue for dataset"

  num_train = len(train_data)
  indices = list(range(num_train))
  split = int(np.floor(args.train_portion * num_train))
  print("Total Training size",num_train)
  print("Training set size",split)
  print("Validation set size",num_train-split)

  if args.dataset == 'devanagari':
    print("SHUFFLE INDEX LIST BEFORE BATCHING")
    print("Before Shuffle", indices[-10:num_train])
    random.shuffle(indices)
    print("After Shuffle", indices[-10:num_train])

  train_queue = torch.utils.data.DataLoader(
      train_data, batch_size=args.batch_size,
      sampler=torch.utils.data.sampler.SubsetRandomSampler(indices[:split]),
      pin_memory=True, num_workers=2)

  valid_queue = torch.utils.data.DataLoader(
      train_data, batch_size=args.batch_size,
      sampler=torch.utils.data.sampler.SubsetRandomSampler(indices[split:num_train]),
      pin_memory=True, num_workers=2)

  return train_queue, valid_queue
