"""Explicit one-time download. Record immutable upstream revisions."""
import json
from huggingface_hub import HfApi, snapshot_download
from .config import model_dir, ROOT

def main():
    root=model_dir(); root.mkdir(parents=True,exist_ok=True)
    manifest_path=root/'manifest.json'
    lock=ROOT/'models.lock.json'
    previous=json.loads(lock.read_text()) if lock.exists() else json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    result={}
    for name,repo in [('encoder','sentence-transformers/all-MiniLM-L6-v2'),('reranker','cross-encoder/ms-marco-MiniLM-L6-v2')]:
        revision=previous.get(name,{}).get('revision') or HfApi().model_info(repo).sha
        snapshot_download(repo_id=repo,revision=revision,local_dir=root/name,
            allow_patterns=['*.json','*.txt','*.safetensors','1_Pooling/*','2_Normalize/*','README.md','LICENSE','LICENSE.txt'],
            ignore_patterns=['onnx/*','openvino/*'])
        result[name]={'repository':repo,'revision':revision}
        print(name,revision,flush=True)
    manifest_path.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__': main()
