fileName = str(input('Write the name of your ifc file: '))

'''Slabs'''
''' Find number and name of floors in model'''
def floor(model):
    level = model.by_type('IfcBuildingStorey')
    floors = []
    for ifc_storey in level:
        floors.append(ifc_storey.Name)
    numberOfFloors = len(floors)
    return floors, numberOfFloors


''' Find all levels represented in model'''
def levelOfSlab(model):
    slabs = model.by_type("IfcSlab")
    slabLevels = []
    for slab in slabs:
        contain = slab.ContainedInStructure
        if len(contain) > 0:
            nameOfFloor = contain[0].RelatingStructure.Name
            slabLevels.append(nameOfFloor)
    return slabLevels


'''Find slab volume and slab area of the different slabs'''
def slabVolumeAndArea(model):
    slabs = model.by_type("IfcSlab")
    numberOfSlabs = len(slabs)
    slabsRequired = 0
    slabsInModel = len(model.by_type("IfcSlab"))
    slabArea = []
    slabVolume = []
    slabThickness = []
    if (slabsRequired <= slabsInModel):    
        for entity in slabs:
            for relDefinesByProperties in entity.IsDefinedBy:
                for slab_prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                    if slab_prop.Name == 'Area':
                        slabArea.append(slab_prop.NominalValue.wrappedValue)

                    elif slab_prop.Name == 'Volume':
                        slabVolume.append(slab_prop.NominalValue.wrappedValue)

                    elif slab_prop.Name == 'Thickness':
                        slabThickness.append(slab_prop.NominalValue.wrappedValue)
    return slabVolume, slabArea, slabThickness, numberOfSlabs


''' Find which slab located in which floor'''
def slabDictionarys(slabLevels, floors, slabArea, slabVolume, slabThickness):
    slabPropertyDict = {}
    for floor in floors:
        currentKey = ()
        # currentSlab = []
        currentFloor = []
        for i in range(len(slabLevels)):
            currentKey = floor
            if slabLevels[i] == floor:
                #slabInLevel.append([slabVolume[i], slabArea[i]])
                currentFloor.append([slabArea[i], slabVolume[i], slabThickness[i]])
        slabPropertyDict[currentKey] = currentFloor
    return slabPropertyDict


''' Main slab function. combines all the functions above in the right order.'''
def slabMain(model):
    #import ifcopenshell
    #model = ifcopenshell.open(model)
    floors, numberOfFloors = floor(model)
    slabLevels = levelOfSlab(model)
    slabVolume, slabArea, slabThickness, numberOfSlabs = slabVolumeAndArea(model)
    slabPropertyDict = slabDictionarys(slabLevels, floors, slabArea, slabVolume, slabThickness)
    return slabPropertyDict, floors, slabVolume, slabArea, slabThickness, numberOfFloors, numberOfSlabs


'''Beams'''
''' Find number and name of floors in model'''
def floor(model):
    level = model.by_type('IfcBuildingStorey')
    floors = []
    for ifc_storey in level:
        floors.append(ifc_storey.Name)
    numberOfFloors = len(floors)
    return floors, numberOfFloors


''' Find all levels represented in model'''
def levelOfBeam(model):
    beams = model.by_type("IfcBeam")
    beamLevels = []
    for beam in beams:
        contain = beam.ContainedInStructure
        if len(contain) > 0:
            nameOfFloor = contain[0].RelatingStructure.Name
            beamLevels.append(nameOfFloor)
    return beamLevels


'''Find volume, area and length of the different beams'''
def beamVolumeAreaLength(model):
    beams = model.by_type("IfcBeam")
    numberOfBeams = len(beams)
    beamsRequired = 1
    beamsInModel = len(model.by_type("IfcBeam"))
    beamArea = []
    beamVolume = []
    beamLength = []
    if (beamsRequired <= beamsInModel):    
        for entity in beams:
            for relDefinesByProperties in entity.IsDefinedBy:
                for beam_prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                    if beam_prop.Name == 'Volume':
                        beamVolume.append(beam_prop.NominalValue.wrappedValue)
                    elif beam_prop.Name == 'Length':
                        beamLength.append(beam_prop.NominalValue.wrappedValue)
        for beam in range(len(beamVolume)):
            beamArea.append(beamVolume[beam]/beamLength[beam])

    return beamVolume, beamArea, beamLength, numberOfBeams


''' Find which floor of all beams'''
def beamDictionarys(beamLevels, floors, beamArea, beamVolume, beamLength):
    beamPropertyDict = {}
    for floor in floors:
        currentKey = ()
        # currentSlab = []
        currentFloor = []
        for i in range(len(beamLevels)):
            currentKey = floor
            if beamLevels[i] == floor:
                #slabInLevel.append([slabVolume[i], slabArea[i]])
                currentFloor.append([beamArea[i], beamVolume[i], beamLength[i]])
        beamPropertyDict[currentKey] = currentFloor
    return beamPropertyDict


''' Main beam function. combines all the functions above in the right order.'''
def beamMain(model):
    floors, numberOfFloors = floor(model)
    beamLevels = levelOfBeam(model)
    beamVolume, beamArea, beamLength, numberOfBeams = beamVolumeAreaLength(model)
    beamPropertyDict = beamDictionarys(beamLevels, floors, beamArea, beamVolume, beamLength)
    return beamPropertyDict, beamVolume, beamArea, beamLength, numberOfBeams


'''Walls'''
''' Find number and name of floors in model'''
def floor(model):
    level = model.by_type('IfcBuildingStorey')
    floors = []
    for ifc_storey in level:
        floors.append(ifc_storey.Name)
    numberOfFloors = len(floors)
    return floors, numberOfFloors


''' Find all levels represented in model'''
def levelOfWall(model):
    walls = model.by_type("IfcWall")
    wallLevels = []
    for wall in walls:
        contain = wall.ContainedInStructure
        if len(contain) > 0:
            nameOfFloor = contain[0].RelatingStructure.Name
            wallLevels.append(nameOfFloor)
    return wallLevels


'''Find volume, area and width of all walls'''
def wallVolumeAreaWidth(model):
    walls = model.by_type("IfcWall")
    numberOfWalls = len(walls)
    wallsRequired = 1
    wallsInModel = len(model.by_type("IfcWall"))
    wallArea = []
    wallVolume = []
    wallWidth = []
    if (wallsRequired <= wallsInModel):    
        for entity in walls:
            for relDefinesByProperties in entity.IsDefinedBy:
                for wall_prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                    if wall_prop.Name == 'Volume':
                        wallVolume.append(wall_prop.NominalValue.wrappedValue)
                    elif wall_prop.Name == 'Width':
                        wallWidth.append(wall_prop.NominalValue.wrappedValue)
        for i in range(len(wallVolume)):
            wallArea.append(wallVolume[i]/wallWidth[i])

    return wallVolume, wallArea, wallWidth, numberOfWalls


''' Find which floor of all beams'''
def wallDictionarys(wallLevels, floors, wallArea, wallVolume, wallWidth):
    wallPropertyDict = {}
    for floor in floors:
        currentKey = ()
        # currentSlab = []
        currentFloor = []
        for i in range(len(wallLevels)):
            currentKey = floor
            if wallLevels[i] == floor:
                #slabInLevel.append([slabVolume[i], slabArea[i]])
                currentFloor.append([wallArea[i], wallVolume[i], wallWidth[i]])
        wallPropertyDict[currentKey] = currentFloor
    return wallPropertyDict


''' Main beam function. combines all the functions above in the right order.'''
def wallMain(model):
    # import ifcopenshell
    # model = ifcopenshell.open(model)
    floors, numberOfFloors = floor(model)
    wallLevels = levelOfWall(model)
    wallVolume, wallArea, wallWidth, numberOfWalls = wallVolumeAreaWidth(model)
    wallPropertyDict = wallDictionarys(wallLevels, floors, wallArea, wallVolume, wallWidth)
    return wallPropertyDict, wallVolume, wallArea, wallWidth, numberOfWalls


'''Columns'''
''' Find number and name of floors in model'''
def floor(model):
    level = model.by_type('IfcBuildingStorey')
    floors = []
    for ifc_storey in level:
        floors.append(ifc_storey.Name)
    numberOfFloors = len(floors)
    return floors, numberOfFloors


''' Find all levels represented in model'''
def levelOfColumn(model):
    columns = model.by_type("IfcColumn")
    columnLevels = []
    for column in columns:
        contain = column.ContainedInStructure
        if len(contain) > 0:
            nameOfFloor = contain[0].RelatingStructure.Name
            columnLevels.append(nameOfFloor)
    return columnLevels


'''Find volume, area and width of all walls'''
def columnVolumeAreaLength(model):
    columns = model.by_type("IfcColumn")
    numberOfColumns = len(columns)
    columnsRequired = 1
    columnsInModel = len(model.by_type("IfcColumn"))
    columnArea = []
    columnVolume = []
    columnLength = []
    if (columnsRequired <= columnsInModel):    
        for entity in columns:
            for relDefinesByProperties in entity.IsDefinedBy:
                for column_prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                    if column_prop.Name == 'Volume':
                        wallVolume.append(column_prop.NominalValue.wrappedValue)
                    elif column_prop.Name == 'Length':
                        wallWidth.append(column_prop.NominalValue.wrappedValue)
        for i in range(len(columnVolume)):
            columnArea.append(columnVolume[i]/columnLength[i])

    return columnVolume, columnArea, columnLength, numberOfColumns


''' Find which floor of all beams'''
def columnDictionarys(columnLevels, floors, columnArea, columnVolume, columnLength):
    columnPropertyDict = {}
    for floor in floors:
        currentKey = ()
        # currentSlab = []
        currentFloor = []
        for i in range(len(columnLevels)):
            currentKey = floor
            if columnLevels[i] == floor:
                #slabInLevel.append([slabVolume[i], slabArea[i]])
                currentFloor.append([columnArea[i], columnVolume[i], columnLength[i]])
        columnPropertyDict[currentKey] = currentFloor
    return columnPropertyDict


''' Main beam function. combines all the functions above in the right order.'''
def columnMain(model):
    # import ifcopenshell
    # model = ifcopenshell.open(model)
    floors, numberOfFloors = floor(model)
    columnLevels = levelOfColumn(model)
    columnVolume, columnArea, columnLength, numberOfColumns = columnVolumeAreaLength(model)
    columnPropertyDict = columnDictionarys(columnLevels, floors, columnArea, columnVolume, columnLength)
    return columnPropertyDict, columnVolume, columnArea, columnLength, numberOfColumns


'''Implementation of the prices from 'inputPricec.csv'.'''
def prices():
    import csv
    with open('inputPrices2.csv', 'r') as inputPrices:
        prices = csv.reader(inputPrices, delimiter=';')
        priceList = list(prices)

    slabPrices = {
        'concrete': {
            'reinforcement': float(priceList[2][2]), # Price per [m^3]
            'concrete': float(priceList[3][2]),        # Price per [m^3]
            'formework': float(priceList[4][2]),        # Price per [m^2] 
            'labour': float(priceList[5][2])            # Price per [m^2]
        },
        'timber': {
            'material': float(priceList[8][2]),         # Price per [m^3]
            'labour': float(priceList[9][2])            # Price per [m^2]
        }
    }

    columnPrices = {
        'concrete': {
            'reinforcement': float(priceList[14][2]), # Price per [m^3]
            'concrete': float(priceList[15][2]),        # Price per [m^3]
            'formework': float(priceList[16][2]),        # Price per [m^2] (parameter) 
            'labour': float(priceList[17][2])           # Price per [m]
        },
        'steel': {
            'material': float(priceList[20][2]),      # Price per [m^3]
            'labour': float(priceList[21][2])           # Price per clumn
        },
        'timber': {
            'material': float(priceList[24][2]),         # Price per [m^3]
            'labour': float(priceList[25][2])          # Price per column

        }
    }

    beamPrices = {
        'concrete': {
            'reinforcement': float(priceList[30][2]), # Price per [m^3]
            'concrete': float(priceList[31][2]),        # Price per [m^3]
            'formework': float(priceList[32][2]),        # Price per [m^2]
            'labour': float(priceList[33][2])           # Price per [m]
        },
        'steel': {
            'material': float(priceList[36][2]),      # Price per [m^3]
            'labour': float(priceList[37][2])           # Price per beam
        },
        'timber': {
            'material': float(priceList[40][2]),         # Price per [m^3]
            'labour': float(priceList[41][2])           # Price per beam
        }
    }

    wallPrices = {
        'concrete': {
            'reinforcement': float(priceList[46][2]), # Price per [m^3]
            'concrete': float(priceList[47][2]),        # Price per [m^3]
            'formework': float(priceList[48][2]),        # Price per [m^2] 
            'labour': float(priceList[49][2])            # Price per [m^2]
        },
        'timber': {
            'material': float(priceList[52][2]),         # Price per [m^3]
            'labour': float(priceList[53][2])            # Price per [m^2]
        }
    }
    return slabPrices, columnPrices, beamPrices, wallPrices


'''Prices of slabs'''
def slabPrice(slabPropertyDict, slabPrices, floors, numberOfSlabs):
    slabFloorPrice = {}
    if numberOfSlabs > 0:
        for f in range(len(floors)):
            floorSlab = (slabPropertyDict[floors[f]])     
            slabPrice = []
            for i in range(len(floorSlab)):
                currentSlab = floorSlab[i]
                reinforcementPrice = 0.01*currentSlab[1]*slabPrices['concrete']['reinforcement']
                concretePrice = currentSlab[1]*slabPrices['concrete']['concrete']
                frameworkPrice = currentSlab[0]*slabPrices['concrete']['formework']
                labourPrice = currentSlab[0]*slabPrices['concrete']['labour']
                totalSlabPrice = reinforcementPrice + concretePrice + frameworkPrice + labourPrice
                slabPrice.append(totalSlabPrice)
            if f == 0:
                for j in range(len(slabPrice)):
                    slabPrice[j] = slabPrice[j]*1.0
            elif 1 <= f <= 9:
                for j in range(len(slabPrice)):
                    slabPrice[j] = slabPrice[j]*(1.2+0.05*(f))
            elif f >= 10:
                for j in range(len(slabPrice)):
                    slabPrice[j] = slabPrice[j]*(1.2+0.05*10+(0.01*(f-10)))
            slabFloorPrice[floors[f]] = slabPrice
    return slabFloorPrice


'''Prices of beams'''
def beamPrice(beamPropertyDict, beamPrices, floors, numberOfBeams):
    beamFloorPrice = {}
    if numberOfBeams > 0:
        for f in range(len(floors)):
            floorBeam = (beamPropertyDict[floors[f]])
            beamPrice = []
            for i in range(len(floorBeam)):
                currentBeam = floorBeam[i]
                steelPrice = currentBeam[1]*beamPrices['steel']['material']
                totalBeamPrice = steelPrice
                beamPrice.append(totalBeamPrice)
            if f == 0:
                for j in range(len(beamPrice)):
                    beamPrice[j] = beamPrice[j]*1.0
            elif 1 <= f <= 9:
                for j in range(len(beamPrice)):
                    beamPrice[j] = beamPrice[j]*(1.2+0.05*(f))
            elif f >= 10:
                for j in range(len(beamPrice)):
                    beamPrice[j] = beamPrice[j]*(1.2+0.05*10+(0.01*(f-10)))
            beamFloorPrice[floors[f]] = beamPrice
    return beamFloorPrice


'''Prices of walls'''
def wallPrice(wallPropertyDict, wallPrices, floors, numberOfWalls):
    wallFloorPrice = {}
    if numberOfWalls > 0:
        for f in range(len(floors)):
        # floorSlab = []
            floorWall = (wallPropertyDict[floors[f]])
            wallPrice = []
        # print(floorSlab)
            for i in range(len(floorWall)):
                currentWall = floorWall[i]
                reinforcementPrice = 0.01*currentWall[1]*wallPrices['concrete']['reinforcement']
                concretePrice = currentWall[1]*wallPrices['concrete']['concrete']
                frameworkPrice = currentWall[0]*wallPrices['concrete']['formework']
                totalWallPrice = reinforcementPrice + concretePrice + frameworkPrice
                wallPrice.append(totalWallPrice)
            if f == 0:
                for j in range(len(wallPrice)):
                    wallPrice[j] = wallPrice[j]*1.0
            elif 1 <= f <= 9:
                for j in range(len(wallPrice)):
                    wallPrice[j] = wallPrice[j]*(1.2+0.05*(f))
            elif f >= 10:
                for j in range(len(wallPrice)):
                    wallPrice[j] = wallPrice[j]*(1.2+0.05*10+(0.01*(f-10)))
            wallFloorPrice[floors[f]] = wallPrice
    return wallFloorPrice


'''Prices of columns'''
def columnPrice(columnPropertyDict, columnPrices, floors, numberOfColumns):
    columnFloorPrice = {}
    if numberOfColumns > 0:
        for f in range(len(floors)):
            floorColumn = (columnPropertyDict[floors[f]])
            columnPrice = []
        # print(floorSlab)
            for i in range(len(floorColumn)):
                currentColumn = floorColumn[i]
                steelPrice = currentColumn[1]*columnPrices['steel']['material']
                totalColumnPrice = steelPrice
                columnPrice.append(totalColumnPrice)
            if f == 0:
                for j in range(len(columnPrice)):
                    columnPrice[j] = columnPrice[j]*1.0
            elif 1 <= f <= 9:
                for j in range(len(columnPrice)):
                    columnPrice[j] = columnPrice[j]*(1.2+0.05*(f))
            elif f >= 10:
                for j in range(len(columnPrice)):
                    columnPrice[j] = columnPrice[j]*(1.2+0.05*10+(0.01*(f-10)))
            columnFloorPrice[floors[f]] = columnPrice
    return columnFloorPrice


def cost(slabPropertyDict, beamPropertyDict, wallPropertyDict, columnPropertyDict, floors, numberOfSlabs, numberOfBeams, numberOfWalls, numberOfColumns):
    slabPrices, columnPrices, beamPrices, wallPrices  = prices()
    slabFloorPrice = slabPrice(slabPropertyDict, slabPrices, floors, numberOfSlabs)
    beamFloorPrice = beamPrice(beamPropertyDict, beamPrices, floors, numberOfBeams)
    wallFloorPrice = wallPrice(wallPropertyDict, wallPrices, floors, numberOfWalls)
    columnFloorPrice = columnPrice(columnPropertyDict, columnPrices, floors, numberOfColumns)
    return slabFloorPrice, beamFloorPrice, wallFloorPrice, columnFloorPrice


def csvPrices(slabFloorPrice, beamFloorPrice, wallFloorPrice, columnFloorPrice, floors, numberOfSlabs, numberOfBeams, numberOfWalls, numberOfColumns):
    import csv
    floors = floors
    with open('cost.csv', 'w') as file:
        writer = csv.writer(file)
        separator = ['sep=,']
        writer.writerow(separator)
        writer.writerow(['All prices is given in Euro (EUR)'])

        '''Slabs'''
        writer.writerow(['Slabs:'])
        if numberOfSlabs > 0:
            writer.writerow(['Price of slabs in each floor:'])
            if numberOfSlabs <= 3:
                n = (0.97**numberOfSlabs)
            elif 3 < numberOfSlabs <= 25:
                n = (0.97**3 - 0.003*(numberOfSlabs-3))
            else:
                n = sumSlabs*0.85
            sumSlabs = 0
            for floor in floors:
                text = [floor]
                slabPrices = slabFloorPrice[floor]
                for slabPrice in slabPrices:
                    text.append(n*slabPrice)
                text.append('Total price of slabs in this floor: ')
                text.append(n*sum(slabPrices))
                writer.writerow(text)
                sumSlabs += n*sum(slabPrices)
            writer.writerow(['Total price of all slabs: ', sumSlabs])

        else:
            writer.writerow(['There are no slabs in the model'])
            sumSlabs = 0


        '''Beams'''
        writer.writerow(['Beams:'])
        if numberOfBeams > 0:
            writer.writerow(['Price of beams in each floor:'])
            if numberOfBeams <= 3:
                n = (0.97**numberOfBeams)
            elif 3 < numberOfBeams <= 25:
                n = (0.97**3 - 0.003*(numberOfBeams-3))
            else:
                n = 0.85
            sumBeams = 0
            for floor in floors:
                text = [floor]
                beamPrices = beamFloorPrice[floor]
                for beamPrice in beamPrices:
                    text.append(n*beamPrice)
                text.append('Total price of beams in this floor: ')
                text.append(n*sum(beamPrices))
                writer.writerow(text)
                sumBeams += n*sum(beamPrices)
            writer.writerow(['Total price of all beams: ', sumBeams])
            
        else:
            writer.writerow(['There are no beams in the model'])
            sumBeams = 0


        '''Walls'''
        writer.writerow(['Walls:'])
        if numberOfWalls > 0:
            writer.writerow(['Price of walls in each floor:'])
            if numberOfWalls <= 3:
                n = (0.97**numberOfWalls)
            elif 3 < numberOfWalls <= 25:
                n = (0.97**3 - 0.003*(numberOfWalls-3))
            else:
                n = 0.85
            sumWalls = 0
            for floor in floors:
                text = [floor]
                wallPrices = wallFloorPrice[floor]
                for wallPrice in wallPrices:
                    text.append(n*wallPrice)
                text.append('Total price of walls in this floor: ')
                text.append(n*sum(wallPrices))
                writer.writerow(text)
                sumWalls += n*sum(wallPrices)
            writer.writerow(['Total price of all walls: ', sumWalls])
            
        else:
            writer.writerow(['There are no walls in the model'])
            sumWalls = 0


        '''Columns'''
        writer.writerow(['Columns:'])
        if numberOfColumns > 0:
            writer.writerow(['Price of columns in each floor:'])
            if numberOfColumns <= 3:
                n = (0.97**numberOfColumns)
            elif 3 < numberOfColumns <= 25:
                n = (0.97**3 - 0.003*(numberOfColumns-3))
            else:
                n = 0.85
            sumColumns = 0
            for floor in floors:
                text = [floor]
                columnPrices = columnFloorPrice[floor]
                for columnPrice in columnPrices:
                    text.append(n*columnPrice)
                text.append('Total price of columns in this floor: ')
                text.append(n*sum(columnPrices))
                writer.writerow(text)
                sumColumns += n*sum(columnPrices)
            writer.writerow(['Total price of all columns: ', sumColumns])
            
        else:
            writer.writerow(['There are no columns in the model'])
            sumColumns = 0


        writer.writerow(['Total:'])
        writer.writerow(['Total price of all load bearing elements: ', sumWalls + sumBeams + sumSlabs + sumColumns, ' given in the same currency as your input'])
        

''' Main function'''
def costEstimation(ifcFileName):
    import ifcopenshell
    model = ifcopenshell.open(ifcFileName)
    slabPropertyDict, floors, slabVolume, slabArea, slabThickness, numberOfFloors, numberOfSlabs = slabMain(model)
    beamPropertyDict, beamVolume, beamArea, beamLength, numberOfBeams = beamMain(model)
    wallPropertyDict, wallVolume, wallArea, wallWidth, numberOfWalls = wallMain(model)
    columnPropertyDict, columnVolume, columnArea, columnLength, numberOfColumns = columnMain(model)
    slabFloorPrice, beamFloorPrice, wallFloorPrice, columnFloorPrice = cost(slabPropertyDict, beamPropertyDict, wallPropertyDict, columnPropertyDict, floors, numberOfSlabs, numberOfBeams, numberOfWalls, numberOfColumns)
    csvPrices(slabFloorPrice, beamFloorPrice, wallFloorPrice, columnFloorPrice, floors, numberOfSlabs, numberOfBeams, numberOfWalls, numberOfColumns)
    return slabPropertyDict, floors, slabVolume, slabArea, slabThickness, numberOfFloors, beamPropertyDict, beamVolume, beamArea, beamLength, wallPropertyDict, wallVolume, wallArea, wallWidth, columnPropertyDict, columnVolume, columnArea, columnLength, slabFloorPrice, beamFloorPrice, wallFloorPrice

slabPropertyDict, floors, slabVolume, slabArea, slabThickness, numberOfFloors, beamPropertyDict, beamVolume, beamArea, beamLength, wallPropertyDict, wallVolume, wallArea, wallWidth, columnPropertyDict, columnVolume, columnArea, columnLength, slabFloorPrice, beamFloorPrice, wallFloorPrice = costEstimation(fileName)
