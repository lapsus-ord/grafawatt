# ⚡️ GrafaWatt

> 📊️ See France (& soon your personal) energy consumption in Grafana

## Start Project

### Install dependencies

```bash
pip install influxdb-client python-dotenv requests

cp .env.dist .env
```

You can change information in `.env` file if you want.  
And don't worry, it will work even if you don't change anything.

### Start influxdb & grafana

```bash
docker compose up -d
```

Grafana: [localhost:3001](http://localhost:3001)   
InfluxDB: [localhost:3002](http://localhost:3002)

### Run application

```bash
python3 main.py
```

> ⚠️ If you have python 3 by default, you can run it with:
> ```bash
> python main.py
> ```

<br>
<hr>

## Resources

- [ODRÉ & RTE personal documentation](./doc)
- [Enedis - Open Data](https://data.enedis.fr/pages/accueil/)
- [Enedis - Data Hub](https://datahub-enedis.fr/)
- [Enedis - Realtime local data](https://datahub-enedis.fr/donnees-aval/)
- [Grafana - Get started with Grafana and InfluxDB](https://grafana.com/docs/grafana/latest/getting-started/get-started-grafana-influxdb/)
- [Grafana - Dashboard JSON model](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/view-dashboard-json-model/)
- [Grafana - InfluxDB Datasource](https://grafana.com/docs/grafana/latest/datasources/influxdb)
- [Grafana - Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [InfluxDB - Key Concepts](https://docs.influxdata.com/influxdb/v2.6/reference/key-concepts/)
- [InfluxDB - Python client library](https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/)
- [InfluxDB - Get started with Flux](https://docs.influxdata.com/influxdb/v2.6/query-data/get-started/)
- [InfluxDB - Flux vs InfluxQL](https://docs.influxdata.com/influxdb/v2.6/reference/syntax/flux/flux-vs-influxql/)
