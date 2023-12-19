from config.production_config import text_recognition_weights_path, text_recognition_config_yml_path

config_yml_path = None
checkpoint_path = None

dataset_params = {
    'name':'PBL6',
    'data_root':'./dataset/',
    'train_annotation':'train_annotation.txt',
    'valid_annotation':'val_annotation.txt'
}

params = {
         'print_every':200,
         'valid_every':15*200,
          'iters':20000,
          'checkpoint': checkpoint_path,    
          'export': text_recognition_weights_path,
          'metrics': 1000
}
