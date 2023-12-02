# System Library
import sys,os

# JSON Library
import json as JSON

# Species Table Data
from species import SPECIES as species

if __name__ == '__main__':

    # Get the arguments, excluding filename
    args = sys.argv[1:]

    # At least one argument
    if len(args) > 0:
        # Loop over arguments
        for arg in args:
            # Get file name
            filename = os.path.basename(arg)

            print(f"Processing file '{filename}' ...")

            try:
                # Get folder path
                folder = os.path.dirname(arg)

                # Empty table
                table = {}

                print(f"Folder: '{folder}' ...")

                # Open the file from the argument
                with open(arg, "r") as file:
                    # Read file contents
                    content = file.read()

                    # Load the json content
                    json = JSON.loads(content)

                    # Loop over all of the keys
                    for key in species.keys():
                        # Start all species with zero
                        table[key] = []

                    # Get wild encounter groups data
                    groups = json["wild_encounter_groups"] 

                    # Wild encounters as the first group
                    wild_encounters = groups[0]

                    # Get the wild encounter fields
                    fields = wild_encounters["fields"]

                    # Get the wild encounter sets
                    encounters = wild_encounters["encounters"]

                    # Loop over the encounters
                    for spawntable in encounters:
                        # Get map name, label
                        map = spawntable["map"]
                        label = spawntable["base_label"]

                        print(f"Processing map {map} [{label}] ...")

                        # Loop over the fields
                        for field in fields:

                            # Get the type from the field
                            field_type = field['type']

                            # If the map has this table
                            if field_type in spawntable:
                                print(f"Info: Processing field type '{field_type}' ...")

                                # Get the mons from the field data
                                mons = spawntable[field_type]["mons"]

                                # Loop over the mons
                                for mon in mons:
                                    
                                    # Get the species from the mon
                                    mon_species = mon['species']

                                    # If the species is in the keys
                                    if mon_species in table.keys():
                                        # Add the label (area) to the species
                                        table[mon_species].append(label)
                                    else:
                                        print(f"Info: Species {mon_species} not found in species database!")
                                    
                            else:
                                print(f"Info: {label} does not have field type '{field_type}'.")

                print("Finished processing maps. Generating report ...")

                # File content, will be joined later
                content = ["Species,Encounters,Routes"]

                # Loop over all of the species in the table
                for table_species in table.keys():
                    # Add the species data to the content array
                    content.append(f"{table_species},{len(table[table_species])},{'|'.join(table[table_species])}")

                # Generate the completed report
                output = '\n'.join(content)

                # Generate encounter report csv filename
                report = os.path.join(folder, "encounter-report.csv")

                print(f"Report finished. Writing to file {report} ...")

                # Open the report file
                with open(report, "w") as r:
                    # Write the report to the file
                    r.write(output)

                print(f"Done. Processing file '{filename}' completed.")

            # Failed for argument
            except Exception as e:
                print(f"Failed to process file '{filename}'! Error: '{str(e)}'")
    else:
        print("usage: analyser.py [path-to-wild-encounters.json]")
