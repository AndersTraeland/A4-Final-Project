import ifcopenshell
model = ifcopenshell.open('Duplex_A_20110907.ifc')


''' Find number and name of floors in model'''
def floor(model):
    level = model.by_type("IfcBuildingStorey")
    floors = []
    for ifc_storey in level:
        floors.append(ifc_storey.Name)
    numberOfFloors = len(floors)
    return floors, numberOfFloors

# floors, numberOfFloors = floor(model)
# print(floors, numberOfFloors)


''' Find all levels represented in model'''
def levelOfSlab(model):
    slabs = model.by_type("IfcSlab")
    levels = []
    for slab in slabs:
        contain = slab.ContainedInStructure
        if len(contain) > 0:
            nameOfFloor = contain[0].RelatingStructure.Name
            levels.append(nameOfFloor)
    return levels

# levels = levelOfSlab(model)
# print(levels)


'''Find slab volume and slab area of the different slabs'''
def slabVolumeAndArea(model):
    slabs = model.by_type("IfcSlab")
    slabsRequired = 0
    slabsInModel = len(model.by_type("IfcSlab"))
    slabArea = []
    slabVolume = []
    if (slabsRequired <= slabsInModel):    
        for entity in slabs:
    #we need to get the attributes
            for relDefinesByProperties in entity.IsDefinedBy:
                for slab_prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
    #and then get the attribute we are looking for
                    if slab_prop.Name == 'Area':
                        slabArea.append(slab_prop.NominalValue.wrappedValue)

                    elif slab_prop.Name == 'Volume':
                        slabVolume.append(slab_prop.NominalValue.wrappedValue)
    return slabVolume, slabArea

# slabVolume, slabArea = slabVolumeAndArea(model)
# print(slabArea)
# print(slabVolume)
slabs = model.by_type("IfcSlab")
slabsRequired = 0
slabsInModel = len(model.by_type("IfcSlab"))
if (slabsRequired <= slabsInModel):
    for entity in model.by_type("IfcSlab"):
        for relDefinesByProperties in entity.IsDefinedBy:
            for slab_prop in relDefinesByProperties.RelatingPropertyDefinition.HasProperties:
                if slab_prop.Name == 'Slab Material':
                    
                    print('they consist of '+str(slab_prop.NominalValue.wrappedValue))


''' Find which slab located in which floor'''
def slabDictionatys(levels, floors, slabArea, slabVolume):
    slabVolumeDict = {}
    slabAreaDict = {}
    for floor in floors:
        currentKey = ()
        areasInLevel = []
        volumesInLevel = []
        for i in range(len(levels)):
            currentKey = floor
            if levels[i] == floor:
                areasInLevel.append(slabArea[i])
                volumesInLevel.append(slabVolume[i])
        slabVolumeDict[currentKey] = volumesInLevel
        slabAreaDict[currentKey] = areasInLevel
    return slabVolumeDict, slabAreaDict

# slabVolumeDict, slabAreaDict = slabDictionatys(levels, floors, slabArea, slabVolume)
# print(slabVolumeDict)
# print(slabAreaDict)


''' Main slab function. combines all the functions above in the right order.'''
def slabMain(model):
    floors, numberOfFloors = floor(model)
    levels = levelOfSlab(model)
    slabVolume, slabArea = slabVolumeAndArea(model)
    slabVolumeDict, slabAreaDict = slabDictionatys(levels, floors, slabArea, slabVolume)
    return slabVolumeDict, slabAreaDict, floors, slabVolume, slabArea, numberOfFloors

slabVolumeDict, slabAreaDict, floors, slabVolume, slabArea, numberOfFloors = slabMain(model)


print(slabVolumeDict)

print(slabAreaDict)

# print(slabVolumeDict[floors[1]])


# Counting number of different slabs in the IFC project








# totalSlabVolume = 0
# for volume in slabVolume:
#     totalSlabVolume = totalSlabVolume + volume
# print(totalSlabVolume)


# walls = model.by_type("IfcWall")
# slabs = model.by_type("IfcSlab")
# #Then do sth I want
# floors = model.by_type("IfcBuildingStorey")
# for wall in walls:
#   contain = wall.ContainedInStructure
#   if len(contain) > 0:
#      if contain[0].RelatingStructure.Name == floors[0]:
#         print(contain[0])