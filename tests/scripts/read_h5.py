import h5py

FILE_NAME = 'ATL06_20181014001920_02350103_001_01'

def main():
    global FILE_NAME
    
    if '.h5' not in FILE_NAME:
        FILE_NAME = "resources\\h5testfiles\\" + FILE_NAME + '.h5'
        
    with h5py.File(FILE_NAME, 'r') as h5_file:
        print(f"Keys: {h5_file.keys()}\n\n")
        
        
        for key in h5_file.keys():
            for subkey in h5_file[key]:
                print(f"Key {key}: Group in {subkey}: {list(h5_file[key][subkey])}")
                for subkey2 in h5_file[key][subkey]:
                    print(f"{list(h5_file[key][subkey][subkey2])}")

if __name__ == "__main__":
    main()