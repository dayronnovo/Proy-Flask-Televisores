from functools import wraps
from flask import jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt


class JwtConfig:
    RSA_PRIVADA = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA51PAmQOQcX99NQ+B2YWI1ZNJAEDgzUW2unPX7ZQ43CsaH9qY
zS0S/DSpC+SXLWMV1nK/qVtxv4W1yNZgMZEhYeTROgBjvJ8lKTAK7Nxnj+UUrNax
pmOZ5WuGSYPbTm8jaUMX8z1YSayuEjj/9puduWyLlXj2EqiWaAYi1EH0WFvjtIIf
rNPONF3AUMeeQu2AnRdOnxoPS8/yi5NPsMr38Hipa5/kF7ZsGlxjnGxi2vTBdzZA
KUdbIrSNY3NubTuuJozYkYy2bOIiWI0A7I47JF9xa6ghgEipfK9fJFK8wpgHmx3a
qecqPjXlFZiYS5YUYQQM2DErZIe+4PtgUvUz4QIDAQABAoIBAQDl1J9hJ1pmeY0T
n8GaNYL692erOcpgCCiBXUEmiYJotOYyycPQ7jyTmVpvN4FAFdcHhmCIShNcfuNa
lCtkc9Yf5fA+WU6+g7uvDU19gYnfPHHrOy+rqf+oIcl81uWYKvGazo9IGyXRpSAZ
eMpO4NO2+3I/YrvRU/CDj70g+BplgZqG3/A1Mwapuu/Fd9J171Qhh7d6OLihiM52
fQk7Fp4/7KbDyjrLotVJBMn6DwI5T6AIVxFRPmKiG/HNQXgaD/z1f3cUzxUefTqL
Glnfsq8YiB+697no/4V9TyxG4+81PBdv2mQTjKehG4863T2hf/D9usV3HUAY8lyi
Ealf908xAoGBAPu/T8iz7nVcN3TJei1CSTVadUgkGaieOT/dF84LaSC3t9tjxfNJ
A8D39LZrGK51oZHXXJVLBdIrfQa3uLSjZMOc8xWiUB48e30NwenIfq6rYnFcyldp
H4Te4gYKT4CLC0SkEhV4C2oYZ/s+H6NqonSErLegK0uxtP2AKTqobHJtAoGBAOs8
IhYIdNMOVDfoempi8/LPoCVeGXI1YqSsCfhTW3VWeQK2dXUwksN+zke71ZS2p7j2
0URUhD1OtYPwA0hR0YKVWL7tV0xikzPiEiiX2VAP9DpNAwS6U1DP/6CYFFRdR85a
6/i5D2tX6obIXoe31x9GM3zLh+RSQ7+ASdkCPf7FAoGADSIm7GaOqyq7belQ6WmK
3jCw66mOeSCABhfntQUdX+qVuelTm2SUwI1vA9FEgV17p1sf5l36mMNSC3asOShJ
Cnd2qwtDuMAZBSYhlquyCDTCtv1LRRIj5c+m5P/GtAMM/HC+zMXteoR5cD8GcYUP
opqFVDMT7yf/NDZqcDf3KGUCgYEAs6Sjn1Hr7bZWqK+YtSBGjprzATaAllCguYNM
xeDaypw0I9c1kj57BmMTo4KV1FE9eyq6m8UzjCJMyqqDxzn8lw34zS4x6fqp0giG
t4tngRX9/HwNnxGwSNnfrUQW2mq2SKf052hklyR3zWC9mEXUOmUBMv+4EqykYl3V
h62HrMUCgYA1uhE8dvpcNRQSVx3lfSrkvEEyaxANT+/N62m5kaFoyB0DRmKzQNVp
IpjRPQlFLhfLGPkN1LUS51Td0EbHUpMnyw+RewwOK/m767zGy4k6qbnI9h3w/csY
s2kWywOtz69qO7nJSCMDuZPYN4IAPwOkyoqz2VZ8UpI940WKERwAMA==
-----END RSA PRIVATE KEY-----"""

    RSA_PUBLICA = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA51PAmQOQcX99NQ+B2YWI
1ZNJAEDgzUW2unPX7ZQ43CsaH9qYzS0S/DSpC+SXLWMV1nK/qVtxv4W1yNZgMZEh
YeTROgBjvJ8lKTAK7Nxnj+UUrNaxpmOZ5WuGSYPbTm8jaUMX8z1YSayuEjj/9pud
uWyLlXj2EqiWaAYi1EH0WFvjtIIfrNPONF3AUMeeQu2AnRdOnxoPS8/yi5NPsMr3
8Hipa5/kF7ZsGlxjnGxi2vTBdzZAKUdbIrSNY3NubTuuJozYkYy2bOIiWI0A7I47
JF9xa6ghgEipfK9fJFK8wpgHmx3aqecqPjXlFZiYS5YUYQQM2DErZIe+4PtgUvUz
4QIDAQAB
-----END PUBLIC KEY-----"""

    LLAVE_SECRETA = '53f41bf244c940d2abec1bd3670fd557'


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            authorities = get_jwt()['sub']['authorities']
            print(authorities)
            if 'admin' in authorities:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper
