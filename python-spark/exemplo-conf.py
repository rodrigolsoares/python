import sys
import os
import flagSync
import compareProcess

from pyspark import SparkContext, SparkConf
from pyspark import AccumulatorParam

os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"]= "/usr/bin/python3"

custom_conf={
            "master":"local[1]",''
            "spark.executor.memory" : "4g",
            "spark.executor.cores" : "4",
            "spark.executor.instances":"1",
            "spark.yarn.keytab" : "path file kerberos",
            "spark.yarn.principal" : "machine yarn principal",
            "appName" : 'APP name'
        }

sc_conf = SparkConf()
sc = sc = SparkContext()

sc_conf.setAppName(custom_conf["appName"])
sc_conf.setMaster(custom_conf["master"])
sc_conf.set('spark.executor.memory', custom_conf["spark.executor.memory"])
sc_conf.set('spark.executor.cores', custom_conf["spark.executor.cores"])
sc_conf.set('spark.yarn.keytab', custom_conf["spark.yarn.keytab"])
sc_conf.set('spark.yarn.principal', custom_conf["spark.yarn.principal"])
sc_conf.set('spark.executor.instances', custom_conf["spark.executor.instances"])


try:
    sc.stop()
    sc = SparkContext(conf=sc_conf)
except:
    sc = SparkContext(conf=sc_conf)


class valueAccumulator(AccumulatorParam):
    def zero(self, s):
        return s
    def addInPlace(self, s1, s2):
        return s1 + s2
