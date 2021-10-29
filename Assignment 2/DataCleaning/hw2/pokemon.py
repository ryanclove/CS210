import csv
from collections import Counter
from collections import defaultdict
def firePokemon():
    with open('pokemonTrain.csv') as pokemon:
        reader = csv.reader(pokemon)
        next(reader)
        fireTypes = 0
        totalPokemon = 0
        for num,row in enumerate(reader):
            totalPokemon += 1
            if row[4] == 'fire':
                fireTypes += 1
        ans = (fireTypes / totalPokemon) * 100
        ans = round(ans)
        out =  str(ans) + '%'
        with open('pokemon1.txt', 'w') as pokemonFile:
            pokemonFile.write(f'Percentage of fire type Pokemons at or above level 40 = {out}')
        

def typeMatching():
    types = ['normal', 'fighting', 'grass', 'fire', 'fairy', 'rock', 'ground', 'water', 'electric', 'bug', 'flying']
    with open('pokemonTrain.csv') as pokemon:
        reader = csv.reader(pokemon)
        header = next(reader)
        #Key is weakness, values are what the key is strong against
        typeMatch = {}
        #Stores csv file rows to iterate over them
        rows = []
        for num,row in enumerate(reader):
            rows.append(row)
        #Match the weakness to the types they are strong against
        for type in types:
            typeCounter = Counter()
            for row in rows:
                if row[5] == type and row[4] != 'NaN':
                    typeCounter.update(row[4].split())
            typeMatch[type] = typeCounter
        #Replace NaN values in Csv file
        with open('pokemonResult.csv','w',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            for row in rows:
                if row[4] == 'NaN':
                    strMax = ""
                    intMax = 0
                    for type in typeMatch[row[5]]:
                        if typeMatch[row[5]][type] > intMax:
                            intMax = typeMatch[row[5]][type]
                            strMax = type
                        elif typeMatch[row[5]][type] == intMax:
                            temp = [type,strMax]
                            temp = sorted(temp)
                            strMax = temp[0]
                        row[4] = strMax
                #Row has been updated, just needs to be written to the new csv file        
                writer.writerow(row)

def avgMatching():
    above40HpAvg = 0
    above40AtkAvg = 0
    above40DefAvg = 0
    below40HpAvg = 0
    below40AtkAvg = 0
    below40DefAvg = 0
    
    above40HpCount = 0
    above40AtkCount = 0
    above40DefCount = 0
    below40HpCount = 0
    below40AtkCount = 0
    below40DefCount = 0
    
    with open('pokemonResult.csv') as pokemon:
        reader = csv.reader(pokemon)
        next(reader)
        for num, row in enumerate(reader):
            if(float(row[2]) > 40):
                if(row[6] != 'NaN'):
                    above40AtkCount += 1
                    above40AtkAvg += float(row[6])
                if(row[7] != 'NaN'):
                    above40DefCount += 1
                    above40DefAvg += float(row[7])
                if(row[8] != 'NaN'):
                    above40HpCount += 1
                    above40HpAvg += float(row[8])
            else:
                if(row[6] != 'NaN'):
                    below40AtkCount += 1
                    below40AtkAvg += float(row[6])
                if(row[7] != 'NaN'):
                    below40DefCount += 1
                    below40DefAvg += float(row[7])
                if(row[8] != 'NaN'):
                    below40HpCount += 1
                    below40HpAvg += float(row[8])
    above40HpAvg = round((above40HpAvg/above40HpCount),1)
    above40AtkAvg = round((above40AtkAvg/above40AtkCount),1)
    above40DefAvg = round((above40DefAvg/above40DefCount),1)
    below40HpAvg = round((below40HpAvg/below40HpCount),1)
    below40AtkAvg = round((below40AtkAvg/below40AtkCount),1)
    below40DefAvg = round((below40DefAvg/below40DefCount),1)
    
    with open('pokemonResult.csv') as pokemon:
        reader = csv.reader(pokemon)
        header = next(reader)
        with open('pokemonResult.csv','w',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            for num, row in enumerate(reader):
                if row[6] == 'NaN':
                    if float(row[2]) > 40:
                        row[6] = above40AtkAvg
                    else:
                        row[6] = below40AtkAvg
                if row[7] == 'NaN':
                    if float(row[2]) > 40:
                        row[7] = above40DefAvg
                    else:
                        row[7] = below40DefAvg
                if row[8] == 'NaN':
                    if float(row[2]) > 40:
                        row[8] = above40HpAvg
                    else:
                        row[8] = below40HpAvg
                writer.writerow(row)

def typePersonality():
    types = []
    rows = []
    typeToPersonality = defaultdict(list)
    with open('pokemonResult.csv') as pokemon:
        reader = csv.reader(pokemon)
        next(reader)
        for num,row in enumerate(reader):
            rows.append(row)
    for row in rows:
        if row[4] != 'NaN' and row[4] not in types:
            types.append(row[4])
    sortedTypes = sorted(types)
    for type in sortedTypes:
        for row in rows:
            if row[4] == type:
                if(row[3] not in typeToPersonality[type]):
                    typeToPersonality[type].append(row[3])
        typeToPersonality[type] = sorted(typeToPersonality[type])  
    with open('pokemon4.txt', 'w') as pokemonFile:
        pokemonFile.write("Pokemon type to personality matching: \n")
        for type in sortedTypes:
            str = f'{type}: '
            for personality in typeToPersonality[type]:
                str += f'{personality}, '
            str = str[:-2]
            pokemonFile.write('\t')
            pokemonFile.write(str + '\n')

def avgHitPoints():
    with open('pokemonResult.csv') as pokemon:
        reader = csv.reader(pokemon)
        next(reader)
        hitPoints = 0
        totalPokemon = 0
        for num,row in enumerate(reader):
            if float(row[9]) == 3.0:
                hitPoints += float(row[8])
                totalPokemon += 1
        if totalPokemon == 0:
            return 'No Stage 3 Pokemon'
        ans = hitPoints / totalPokemon
        ans = round(ans)
    with open('pokemon5.txt', 'w') as pokemonFile:
        pokemonFile.write(f'Average hit point for Pokemons of stage 3.0 = {ans}')
def main():
    firePokemon()
    typeMatching()
    avgMatching()
    typePersonality()
    avgHitPoints();
    
if __name__ == "__main__":
    main()