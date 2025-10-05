FROM python:3.13.7-slim AS python-prepared

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


FROM python-prepared AS build 

WORKDIR /factory

COPY pyproject.toml /factory/
RUN python3.13 -m pip install .[build]

COPY rag /factory/rag
RUN python3.13 -m build -C=--global-option=egg_info -C=--global-option=--tag-build="+build"


FROM python-prepared AS deploy

WORKDIR /app

COPY --from=build /factory/dist /dist/
RUN python3.13 -m pip install architecture-rag -f /dist

ENTRYPOINT [ "python3.13", "-m", "architecture-rag"]
