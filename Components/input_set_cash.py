from dash import dcc,html

ddc_Cash_Input = dcc.Input(id='set_cash', value=0, type="number",
                placeholder='Set Cash', debounce= True, min=0, 
                minLength=0, maxLength=50,required=True)