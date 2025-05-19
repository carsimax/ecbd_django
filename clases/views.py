from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import io
import contextlib
import pandas as pd
import numpy as np
import traceback
import os
import json
import tabulate

def landing(request):
    return render(request, 'clases/landing.html')

def clase_carga_exploracion(request):
    return render(request, 'clases/clase_carga_exploracion.html')

def clase_tipos_fuentes_datos(request):
    return render(request, 'clases/clase_tipos_fuentes_datos.html')

@csrf_exempt
def ejecutar_codigo(request):
    if request.method == 'POST':
        try:
            # Importar pandas y numpy para asegurar su disponibilidad
            import pandas as pd
            import numpy as np
            
            data = json.loads(request.body.decode('utf-8'))
            code = data.get('code', '')
            local_vars = {}
            output = io.StringIO()
            # Cargar el DataFrame si se usa 'df' en el código
            if 'df' in code:
                csv_path = os.path.join(os.path.dirname(__file__), 'clientes_pedidos.csv')
                try:
                    local_vars['df'] = pd.read_csv(csv_path)
                except Exception as e:
                    output.write(f"Error al cargar el archivo CSV: {str(e)}")
            with contextlib.redirect_stdout(output):
                exec(code, {'pd': pd, 'np': np, 'tabulate': tabulate.tabulate}, local_vars)
            result = output.getvalue()
            # Mejorar la visualización de DataFrames y salidas
            if 'df' in local_vars:
                code_stripped = code.strip()
                if not result.strip():
                    # Casos comunes
                    if code_stripped.endswith('df'):
                        result += '\n' + tabulate.tabulate(local_vars['df'].head(), headers='keys', tablefmt='fancy_grid', showindex=True)
                    elif code_stripped.endswith('df.head()'):
                        result += '\n' + tabulate.tabulate(local_vars['df'].head(), headers='keys', tablefmt='fancy_grid', showindex=True)
                    elif code_stripped.endswith('df.tail()'):
                        result += '\n' + tabulate.tabulate(local_vars['df'].tail(), headers='keys', tablefmt='fancy_grid', showindex=True)
                    elif code_stripped.endswith('df.shape'):
                        result += '\n' + str(local_vars['df'].shape)
                    elif code_stripped.endswith('df.info()'):
                        buf = io.StringIO()
                        local_vars['df'].info(buf=buf)
                        result += '\n' + buf.getvalue()
                    elif code_stripped.startswith('df.describe(') or code_stripped == 'df.describe()':
                        result += '\n' + tabulate.tabulate(local_vars['df'].describe(include='all'), headers='keys', tablefmt='fancy_grid', showindex=True)
                    elif code_stripped.endswith('df.columns'):
                        result += '\n' + str(list(local_vars['df'].columns))
                    elif code_stripped.endswith('df.dtypes'):
                        result += '\n' + str(local_vars['df'].dtypes)
                    # Casos generales: evaluar la última expresión si no hay print
                    else:
                        try:
                            # Evalúa la última línea si es una expresión
                            last_line = code_stripped.split('\n')[-1]
                            val = eval(last_line, {'pd': pd, 'np': np, 'tabulate': tabulate.tabulate}, local_vars)
                            if isinstance(val, pd.DataFrame):
                                result += '\n' + tabulate.tabulate(val.head(), headers='keys', tablefmt='fancy_grid', showindex=True)
                            elif isinstance(val, pd.Series):
                                result += '\n' + tabulate.tabulate(val.to_frame().head(), headers='keys', tablefmt='fancy_grid', showindex=True)
                            elif isinstance(val, (float, int, str, bool, np.generic)):
                                result += '\n' + str(val)
                        except Exception:
                            pass
            # Si la salida está vacía, mostrar mensaje
            if not result.strip():
                result = 'Sin salida'
            return JsonResponse({'output': result})
        except Exception as e:
            return JsonResponse({'output': 'Error:\n' + traceback.format_exc()})
    return JsonResponse({'output': 'Método no permitido'})

def clase_data_warehouse(request):
    return render(request, 'clases/clase_data_warehouse.html')

def clase_diseno_dw_libreria(request):
    return render(request, 'clases/clase_diseno_dw_libreria.html')

def clase_caso_estudio_dw(request):
    return render(request, 'clases/clase_caso_de_Estudio_dw.html')
