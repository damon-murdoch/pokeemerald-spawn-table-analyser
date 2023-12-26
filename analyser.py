# System Library
import sys,os

# JSON Library
import json as JSON

# Species Table Data
from species import SPECIES as species

# Config file
import config as CONFIG

if __name__ == '__main__':

    # No output methods specified in config
    if CONFIG.OUTPUT_CSV == CONFIG.OUTPUT_MD == None:
        print(f"Error: Please ensure at least one of OUTPUT_CSV and OUTPUT_MD are specified in the config!")

    # Get the arguments, excluding filename
    args = sys.argv[1:]

    # Argument count
    argc = len(args)

    # At least one argument
    if argc > 0:

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

                print("Finished processing maps. Generating reports ...")

                # Get the output directory from the config
                outdir = CONFIG.OUTPUT_DIRECTORY

                # Source folder is specified
                if outdir == 'source_folder':
                    # Set outdir to input folder
                    outdir = folder
                else: # Other folder specified

                    # Ensure no report overlapping occurs

                    # More than one argument
                    if argc > 0:
                        print(f"Warning: Multiple arguments, reports will be placed in {folder} ...")
                        # Set outdir to input folder
                        outdir = folder

                    else: # Just one argument
                        # Ensure directory exists
                        os.makedirs(outdir, exist_ok=True)

                # Get csv filename from config
                csv = CONFIG.OUTPUT_CSV

                # Csv not set to none
                if csv != None:

                    print(f"Generating csv report ...")

                    # File content, will be joined later
                    content = ["Species,Encounters,Routes"]

                    # Loop over all of the species in the table
                    for table_species in table.keys():
                        # Add the species data to the content array
                        content.append(f"{table_species},{len(table[table_species])},{'|'.join(table[table_species])}")

                    # Generate the completed report
                    output = '\n'.join(content)

                    # Build encounter report filename
                    report = os.path.join(outdir, csv)

                    print(f"Writing csv report to file {report} ...")

                    # Open the report file
                    with open(report, "w") as r:
                        # Write the report to the file
                        r.write(output)

                # Get markdown filename from config
                md = CONFIG.OUTPUT_MD

                # Markdown not set to none
                if md != None:

                    print(f"Generating markdown report ...")

                    # File content, will be joined later
                    content = [
                        "| Species | Encounters | Routes |", 
                        "| ------- | ---------- | ------ |"
                    ]

                    # Loop over all of the species in the table
                    for table_species in table.keys():

                        # Get the number of encounters
                        num_encounters = len(table[table_species])

                        # Get the list of encounters
                        encounter_list = ', '.join(table[table_species])

                        # At least one encounter
                        if num_encounters == 0:
                            # Set encounter list to 'None'
                            encounter_list = 'None'

                        # Add the species data to the content array
                        content.append(f"| {table_species} | {num_encounters} | {encounter_list} |")

                    # Generate the completed report
                    output = '\n'.join(content)

                    # Build encounter report filename
                    report = os.path.join(outdir, md)

                    print(f"Writing markdown report to file {report} ...")

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
