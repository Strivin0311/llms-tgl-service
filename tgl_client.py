import os
import argparse
import json
import subprocess



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TGL client script to interact with the model using curl after the docker server is running")
    
    parser.add_argument("--prompt", type=str, required=True, help="The prompt to query to the model")
    
    args, gen_args = parser.parse_known_args()
    
    gen_kwargs = dict()
    for arg in gen_args:
        k, v = arg.split('=')
        
        try: v = float(v)
        except ValueError as fe:
            try: v = int(v)
            except ValueError as ie:
                pass
                
        gen_kwargs[k.replace("--", "")] = v
        
    curl_command = [
        "curl", "127.0.0.1:8080/generate",
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"inputs" : args.prompt,"parameters" : gen_kwargs})
    ]
    
    try:
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Some Error happened when querying the model:\n{e.stderr}")
    
    