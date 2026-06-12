necesito que integres la base de datos con estos paramtros


DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'veterinaria',
        'USER': 'sa',
        'PASSWORD': 'Coto.2025!',
        'HOST': '127.0.0.1',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}


y que hasgas los inserts necesarios, la base de datos esta vacia