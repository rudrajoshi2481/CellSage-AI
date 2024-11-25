#!/bin/bash

# List of packages to uninstall
PACKAGES=(
    aiohappyeyeballs aiohttp aiosignal alembic anndata annotated-types anyio appdirs
    array_api_compat asgiref asttokens async-timeout attrs auth0-python backoff bcrypt
    beautifulsoup4 bleach boto3 botocore Brotli build CacheControl cachetools certifi
    cffi charset-normalizer chroma-hnswlib chromadb cleo click cohere coloredlogs comm
    contourpy crashtest crewai crewai-tools cryptography cycler dataclasses-json debugpy
    decorator defusedxml Deprecated deprecation dill distlib docker docstring_parser
    docx2txt duckduckgo_search dulwich durationpy embedchain exceptiongroup executing
    fastapi fastavro fastjsonschema filelock flatbuffers fonttools frozenlist fsspec
    google-api-core google-auth google-cloud-aiplatform google-cloud-bigquery
    google-cloud-core google-cloud-resource-manager google-cloud-storage google-crc32c
    google-resumable-media googleapis-common-protos gptcache greenlet grpc-google-iam-v1
    grpcio grpcio-status grpcio-tools h11 h2 h5py hpack httpcore httptools httpx
    httpx-sse huggingface-hub humanfriendly hyperframe imageio imageio-ffmpeg
    importlib_metadata importlib_resources iniconfig installer instructor ipykernel
    ipython jaraco.classes jedi Jinja2 jiter jmespath joblib json_repair jsonpatch
    jsonpickle jsonpointer jsonref jsonschema jsonschema-specifications jupyter_client
    jupyter_core jupyterlab_pygments keyring kiwisolver kubernetes lancedb langchain
    langchain-cohere langchain-community langchain-core langchain-experimental
    langchain-ollama langchain-openai langchain-text-splitters langchain-tools langsmith
    legacy-api-wrap litellm llvmlite lxml Mako markdown-it-py MarkupSafe marshmallow
    matplotlib matplotlib-inline mdurl mem0ai mistune mmh3 monotonic moviepy mpmath
    msgpack multidict mutagen mypy-extensions natsort nbclient nbconvert nbformat neo4j
    nest-asyncio networkx nodeenv numba numpy nvidia-cublas-cu11 nvidia-cuda-cupti-cu11
    nvidia-cuda-nvrtc-cu11 nvidia-cuda-runtime-cu11 nvidia-cudnn-cu11 nvidia-cufft-cu11
    nvidia-curand-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11 nvidia-nccl-cu11
    nvidia-nvtx-cu11 oauthlib ollama onnxruntime openai opentelemetry-api
    opentelemetry-exporter-otlp-proto-common opentelemetry-exporter-otlp-proto-grpc
    opentelemetry-exporter-otlp-proto-http opentelemetry-instrumentation
    opentelemetry-instrumentation-asgi opentelemetry-instrumentation-fastapi
    opentelemetry-proto opentelemetry-sdk opentelemetry-semantic-conventions
    opentelemetry-util-http orjson outcome overrides packaging pandas pandocfilters
    parameterized parso patsy pbr pendulum pexpect pillow pkginfo platformdirs pluggy
    poetry poetry-core poetry-plugin-export portalocker posthog prefect primp proglog
    prompt_toolkit proto-plus protobuf psutil ptyprocess pulsar-client pure_eval py
    pyarrow pyasn1 pyasn1_modules pycparser pycryptodomex pydantic pydantic-settings
    pydantic_core Pygments PyJWT pylance pynndescent pypdf PyPika pyproject_hooks
    pyright pysbd PySocks pytest python-dateutil python-decouple python-dotenv pytube
    pytz pytzdata pyvis PyYAML pyzmq qdrant-client qiskit qiskit-aer rank-bm25
    RapidFuzz ratelimiter rdkit referencing regex requests requests-oauthlib
    requests-toolbelt retry rich rpds-py rsa rustworkx s3transfer scanpy schema
    scikit-learn scipy seaborn selenium semver session_info shapely shellingham sniffio
    sortedcontainers soupsieve SQLAlchemy stack-data starlette statsmodels stdlib-list
    stevedore symengine sympy tabulate tenacity threadpoolctl tiktoken tinycss2
    tokenizers tomli tomli_w tomlkit torch torchaudio torchvision tornado tqdm
    traitlets trio trio-websocket triton trove-classifiers typer types-requests
    typing-inspect typing_extensions tzdata umap-learn urllib3 uv uvicorn uvloop
    virtualenv watchfiles wcwidth webencodings websocket-client websockets wrapt wsproto
    xxhash yarl yt-dlp
)

# Uninstall each package
for package in "${PACKAGES[@]}"; do
    echo "Uninstalling $package..."
    pip uninstall -y "$package"
done

echo "All packages have been uninstalled."
