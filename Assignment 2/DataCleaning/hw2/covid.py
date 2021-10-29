import re
import csv
from collections import Counter
from collections import defaultdict

def importRows():
    with open('covidTrain.csv') as covid:
        reader = csv.reader(covid)
        rows = []
        for num, row in enumerate(reader):
            rows.append(row)
        return rows

def ageRange(rows):
    for row in rows:
        res = re.search('[0-9]+-[0-9]+', row[1])
        sum = 0
        if res:
            ages = row[1].split('-')
            for age in ages:
                sum += int(age)
            row[1] = round(sum / 2)
    return rows

def dateChangeHelper(lstDate):
    return f'{lstDate[1]}.{lstDate[0]}.{lstDate[2]}'

def dateChange(rows):
    for row in rows:
        for i in range(8,11):
            row[i] = dateChangeHelper(row[i].split('.'))
    return rows 

def avgCalc(rows, pos):
    provinceDict = {}
    provinceNumValid = {}
    provinceAvg = {}
    for row in rows:
        if row[pos] != 'NaN':
            if row[4] not in provinceDict:
                provinceDict[row[4]] = 0
                provinceNumValid[row[4]] = 0
            provinceDict[row[4]] += float(row[pos])
            provinceNumValid[row[4]] += 1
    for province in provinceDict:
        provinceAvg[province] = round((provinceDict[province] / provinceNumValid[province]),2)
        provinceAvg[province] = "{:.2f}".format(provinceAvg[province])
    return provinceAvg

def provinces(rows):
    provinceLatAvg = avgCalc(rows,6)
    provinceLongAvg = avgCalc(rows, 7)
    for row in rows:
        if row[6] == 'NaN':
            row[6] = provinceLatAvg[row[4]]
        if row[7] == 'NaN':
            row[7] = provinceLongAvg[row[4]]
    return rows

def repCities(rows):
    provinceList = []
    citiesByProvince = {}
    for row in rows:
        if row[4] not in provinceList:
            provinceList.append(row[4])
    for province in provinceList:
        cityCounter = Counter()
        for row in rows:
            if row[4] == province and row[3] != 'NaN':
                cityCounter.update(row[3].split(','))
        citiesByProvince[province] = cityCounter
    for row in rows:
        if row[3] == 'NaN':
            max = 0
            maxCity = ''
            for cities in citiesByProvince[row[4]]:
                if citiesByProvince[row[4]][cities] > max:
                    max = citiesByProvince[row[4]][cities]
                    maxCity = cities
                elif citiesByProvince[row[4]][cities] == max:
                    temp = [maxCity, cities]
                    temp = sorted(temp)
                    maxCity = temp[0]
                else:
                    break
            row[3] = maxCity
    return rows

def provSymptoms(rows):
    provinceList = []
    symptomsByProvince = {}
    for row in rows:
        if row[4] not in provinceList:
            provinceList.append(row[4])
    for province in provinceList:
        symptomCounter = Counter()
        for row in rows:
            if row[4] == province and row[11] != 'NaN':
                list = row[11].split(';')
                for symptom in list:
                    symptom = symptom.lstrip()
                    symptomCounter.update(symptom.split(';'))
        symptomsByProvince[province] = symptomCounter
    for row in rows:
        if row[11] == 'NaN':
            max = 0
            maxSymptom = ''
            for symptoms in symptomsByProvince[row[4]]:
                if symptomsByProvince[row[4]][symptoms] > max:
                    max = symptomsByProvince[row[4]][symptoms]
                    maxSymptom = symptoms
                elif symptomsByProvince[row[4]][symptoms] == max:
                    temp = [maxSymptom, symptoms]
                    temp = sorted(temp)
                    maxSymptom = temp[0]
                else:
                    break
            row[11] = maxSymptom
    return rows
                

def main():
    rows = importRows()
    header = rows[0]
    rows = rows[1:]
    rows = ageRange(rows)
    rows = dateChange(rows)
    rows = provinces(rows)
    rows = repCities(rows)
    rows = provSymptoms(rows)
    with open('covidResults.csv', 'w') as covid:
        writer = csv.writer(covid, delimiter=',')
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
if __name__ == "__main__":
    main()