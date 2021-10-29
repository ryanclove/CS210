import re

def readFromFile(file):
    fromFile = []
    for line in open(file):
        fromFile.extend(line.split())
    return fromFile

def clean(file):
    dirtyWords = readFromFile(file)
    cleanWords = []
    for word in dirtyWords:
        if "https://" in word:
            continue
        if "http://" in word:
            continue
        cleanWord = re.sub(r'[^\w\s]','',word)
        cleanWord = cleanWord.lower()
        cleanWords.append(cleanWord)
    return cleanWords

def removeNoise(cleanWords):
    stopWords = readFromFile('stopwords.txt')
    noStopWords = []
    for word in cleanWords:
        if word in stopWords:
            continue
        else:
            noStopWords.append(word)
    return noStopWords
        
def stemming(words):
    for i,word in enumerate(words):
        if word.endswith('ing'):
            words[i] = word[:-3]
        elif word.endswith('ly'):
            words[i] = word[:-2]
        elif word.endswith('ment'):
            words[i] = word[:-4]
    return words

def writePreProc(file,noStems):
    newFile = "preproc_" + file
    output = open(newFile, 'w')
    for word in noStems:
        word = word + ' '
        output.write(word)
    output.close()
    return newFile

def uniqueWordGenerator(processedFiles):
    uniqueWords = set()
    for file in processedFiles:
        words = readFromFile(file)
        uniqueWords = uniqueWords.union(set(words))
    return uniqueWords

def docWordOccurs(processedFiles):
    i = 0
    lstOfDicts = []
    uniqueWords = uniqueWordGenerator(processedFiles)
    for file in processedFiles:
        ds = dict.fromkeys(uniqueWords, 0)
        words = readFromFile(file)
        for word in words:
            ds[word] += 1
        i += 1
        lstOfDicts.append(ds)
    return lstOfDicts 
        
def computeTF(wordDict, doc):
    tfDict = {}
    wordsInDoc = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count / float(wordsInDoc)
    return tfDict
        
def computeTFHelper(processedFiles):
    lstOfDicts = docWordOccurs(processedFiles)
    tfDictList = []
    for num, file in enumerate(processedFiles):
        words = readFromFile(file)
        tfDictList.append(computeTF(lstOfDicts[num], words))
    return tfDictList

def computeIDF(processedFiles):
    lstOfDicts = docWordOccurs(processedFiles)
    import math
    N = len(lstOfDicts)
    
    idfDict = dict.fromkeys(lstOfDicts[0].keys(),0)
    for d in lstOfDicts:
        for word,val in d.items():
            if val > 0:
                idfDict[word] += 1
    for word, val in idfDict.items():
        idfDict[word] = math.log(N/float(val))
        idfDict[word] += 1
    return idfDict

def computeTFIDFHelper(processedFiles):
    idfs = computeIDF(processedFiles)
    tfDictList = computeTFHelper(processedFiles)
    tfidfList = []
    for d in tfDictList:
        tfidfList.append(computeTFIDF(d, idfs))
    return tfidfList

def computeTFIDF(tfWords, idfs):
    tfidf = {}
    for word, val in tfWords.items():
        tfidf[word] = round(val * idfs[word],2)
    return tfidf
   
    
def writeTFIDF(processedFiles, tfidfList):
    masterList = zip(processedFiles, tfidfList)
    for file, dic in masterList:
        outFile = 'tfidf_' + file
        output = open(outFile, 'w')
        sortedDict = sorted(dic.items(), key = lambda x : (-x[1],x[0]))
        writeOut = '['
        for word, value in sortedDict[:5]:
            writeOut += f"('{word}', {value}), "
        writeOut = writeOut[0:-2]
        writeOut += ']'
        output.write(writeOut)
        output.close()
def main():
    processedFiles = []
    files = []
    for file in open("tfidf_docs.txt",'r'):
        file=file.strip()
        cleanWords = clean(file)
        noStopWords = removeNoise(cleanWords)
        noStems = stemming(noStopWords)
        processedFiles.append(writePreProc(file, noStems))
        files.append(file)
    tfidfList = computeTFIDFHelper(processedFiles)
    writeTFIDF(files, tfidfList)
    
if __name__ == "__main__":
    main()