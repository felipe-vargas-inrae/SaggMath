import pandas as pd

plants_dataset = pd.read_csv("../plants_pheno.csv")

print(plants_dataset.head())


plants_dataset = plants_dataset[["Pot", "Manip", "Area", "Scenario","Sowing", "Harvesting"]]
plants_dataset = plants_dataset.drop_duplicates()
print(plants_dataset.head())


plants_dataset.to_csv("../plant_metadata.csv", index=False)


plants_dataset = plants_dataset[["Area"]]
plants_dataset = plants_dataset.drop_duplicates()
print(plants_dataset)