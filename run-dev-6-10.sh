#!/bin/bash

# Define the paths to the input files and the base output directory
base_conllu_path="/mnt/kesha/seq-labeling-supertags/UD_English-EWT"
base_predictions_path="/mnt/kesha/neural-supertagging/output/eng-ewt"
base_output_path="eng-ewt-ud"  # Root output path
depths=(6 7 8 9 10)

# Loop over the datasets (dev) and depths (6 to 10)
for dataset in dev; do
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

