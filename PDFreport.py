import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker
from fpdf import FPDF

def create_regchart(df, fname, pst):
    fig, ax = plt.subplots()
    
    
    for key, value in years.items():
        ax.plot(df['day_dt'],df[key], color=value[1], linestyle=value[2], label=value[0])
    
    ax.yaxis.grid(lw=0.5)
    ax.yaxis.get_major_ticks()[1].label1.set_visible(False)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    ax.set_facecolor(background_color)
    ax.tick_params(left=False,bottom=False)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    fig.set_size_inches(figsize)
    
    
    plt.tight_layout()
    plt.savefig(f'C:/Users/Misc/{fname}.png',dpi=200, facecolor=background_color)
    plt.close()
    pdf.image(f'C:/Users/Misc/{fname}.png',20,pst,width - 40)
    

cols = ['Version','day_dt','de']

E = pd.read_csv(r'', thousands=',', parse_dates=['day_dt'],infer_datetime_format='%d/%m/%Y').sort_values(by='day_dt')
E.reset_index(drop=True, inplace=True)
E.loc[:, ['day_dt']] = pd.to_datetime(E['day_dt']).dt.strftime('%d-%b')

L = pd.read_csv(r'', thousands=',', parse_dates=['day_dt'],infer_datetime_format='%d/%m/%Y').sort_values(by='day_dt')
L.reset_index(drop=True, inplace=True)
L.loc[:, ['day_dt']] = pd.to_datetime(L['day_dt']).dt.strftime('%d-%b')

A = pd.read_csv(r'C:\Users\e771y6\Desktop\Misc\A_DataCharts_Clean.csv', thousands=',', parse_dates=['day_dt'],infer_datetime_format='%d/%m/%Y').sort_values(by='day_dt')
A.reset_index(drop=True, inplace=True)
A.loc[:, ['day_dt']] = pd.to_datetime(A['day_dt']).dt.strftime('%d-%b')

years = {
  "PYFS2_Days": ["2019 FS", "#2F5597", "solid"],
  "PY2_Days": ["2019", "#2F5597", "dotted"],
  "PYFS1_Days": ["2020 FS", "#FFC000", "solid"],
  "PY1_Days": ["2020", "#FFC000", "dotted"],
  "PYFS_Days": ["2021 FS", "#203864", "solid"],
  "PY_Days": ["2021", "#203864", "dotted"],
  "CYFS_Days": ["2022 FS", "#C55A11", "solid"],
  "CY_Days": ["2022", "#C55A11", "dotted"]
}

width = 210 + 40
height = 297

pdf = FPDF('P', 'mm', (width, height))
pdf.add_page()
pdf.set_font('Arial','B',16)
pdf.cell(75,10,'Title', border='B')
pdf.ln(15)
pdf.set_font('Arial', size=14)
pdf.cell(40,10,'E')
pdf.ln(80)
pdf.set_font('Arial', size=14)
pdf.cell(40,10,'L')
pdf.ln(80)
pdf.set_font('Arial', size=14)
pdf.cell(40,10,'A')

background_color= '#F1EEEF'    
figsize =[10.65,2.64]

create_regchart(E, 'fig1', 40)
create_regchart(L, 'fig2', 120)
create_regchart(A, 'fig3', 200)


pdf.output('C://test1.pdf','F')

