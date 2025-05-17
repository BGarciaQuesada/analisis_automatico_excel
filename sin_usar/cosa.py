# Extraer filas objetivo en cada subsección
        #    for subseccion in self.subsecciones:
        #        start_idx = subsecciones_indices[subseccion][0]
        #        end_idx = start_idx + 1  # Comenzar justo después de la subsección
        #
        #       # Encontrar el final de la subsección actual
        #        while end_idx < len(df_seccion) and df_seccion.iloc[end_idx, 0] not in self.subsecciones:
        #            end_idx += 1
        #
        #        # Extraer solo las filas de la subsección actual
        #        df_subseccion = df_seccion.iloc[start_idx:end_idx]
        #
        #        # Filtrar filas objetivo dentro de la subsección específica
        #        df_filtrado = df_subseccion[df_subseccion.iloc[:, 0].isin(self.filas_objetivo)]
        #        df_final = pd.concat([df_final, df_filtrado])