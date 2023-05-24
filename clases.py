# Primera Transformación de los datos: Eliminar algunas columnas 
class columnDropTransform():
    def __init__(self, columns):
        '''
        columns: lista de columnas a eliminar
        '''
        self.columns = columns
    
    def fit(self, X, y=None):             
        return self
    
    def transform(self, X, y=None):
        return X.drop(self.columns, axis=1) 
    
# Segunda Transformación de los datos: Binzarizar una columna (convertir variables numéricas en variables binarias (0 o 1) en función de un umbral o criterio específico)
class columBinarizeTransform():
    def __init__(self, column, threshold):  
        '''
        column: columna a binarizar
        threshold: umbral para binarizar la columna
        '''        
        self.column = column
        self.threshold = threshold
    
    def fit(self, X, y=None):             
        return self
    
    def transform(self, X, y=None):
        X[self.column] = X[self.column].apply(lambda x: 1 if x >= self.threshold else 0)
        return X

