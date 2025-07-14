import os
from pathlib import Path
import sys
import shutil
import subprocess
import json

def find_root_dir(target_folder_name):
    """
    Busca el directorio raíz del proyecto para el nombre de carpeta especificado.
    """
    current = Path(__file__).resolve()
    while current.name != target_folder_name:
        if current.parent == current:
            raise FileNotFoundError(
                f"No se encontró el directorio '{target_folder_name}' hacia arriba desde {__file__}"
            )
        current = current.parent
    return current


root_dir = find_root_dir("ES_DS-20211374B")

fixtures_dir = root_dir / "fixtures"

if fixtures_dir.exists() and fixtures_dir.is_dir():
    shutil.rmtree(fixtures_dir)

fixtures_dir.mkdir()

def collect_metrics():
    with open(fixtures_dir / f"metrics.csv", "a", encoding="utf-8") as metric_files:
        try:
            metrics_result = subprocess.run(
                    ["kubectl", "top", "pod", "--all-namespaces", "--no-headers"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
            metric_files.write(metrics_result.stdout)
            lines = metrics_result.stdout.strip().split("\n")
            if len(lines) > 1:
                headers = lines[0].split()
                metrics = []

                for line in lines[1:]:
                    values = line.split()
                    metrics.append(dict(zip(headers, values)))

                json_path = fixtures_dir / f"metrics.json"
                with open(json_path, "w", encoding="utf-8") as jf:
                    json.dump(metrics, jf, indent=2)
        except subprocess.CalledProcessError as e:
                print(
                    f"Error al obtener métricas de los pods: {e.stderr}"
                )
        

def del_csv():
    csv_file = fixtures_dir / f"metrics.csv"
    # print(csv_file.is_file())
    os.remove(csv_file)
    #shutil.rmtree(csv_file)

def main ():
    collect_metrics()
    del_csv()

if __name__ == "__main__":
    main()