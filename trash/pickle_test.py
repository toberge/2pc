import pickle

if __name__ == "__main__":
    ledger = []
    try:
        with open('ledger.pickle', 'rb') as ledger_file:
            ledger = pickle.load(ledger_file)
    except Exception as e:
        print('oh well no ledger stored', str(e))

    ledger.append('e')
    print(ledger)
    
    with open('ledger.pickle', 'wb') as ledger_file:
        pickle.dump(ledger, ledger_file)
