#!/bin/bash

# Define the paths to the input files and the base output directory
base_conllu_path="/mnt/kesha/seq-labeling-supertags/UD_English-EWT"
base_predictions_path="/mnt/kesha/neural-supertagging/output/en-ewt"
base_output_path="en-ewt-ud-no-dupe"  # Root output path
depths=(0 1 2 3 4 5)

# Loop over the datasets (train, dev, test) and depths (0 to 5)
for dataset in train dev test; do
    for depth in "${depths[@]}"; do
        # Construct the full paths for the input files
        conllu_file="${base_conllu_path}/en_ewt-ud-${dataset}.conllu"
        predictions_file="${base_predictions_path}-${dataset}/predictions.txt"
        
        # Construct the output directory and ensure it exists
        output_dir="${base_output_path}/${dataset}/"
        mkdir -p "$output_dir"

        # Execute the Python script with the current parameters
        echo "Running replace_tags.py for ${dataset} with depth ${depth}..."
        python replace_tags.py "$conllu_file" "$predictions_file" "$output_dir" "$depth"

        echo "Finished processing ${dataset} with depth ${depth}."
    done
done

