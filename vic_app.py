#%%
import streamlit as st
import yfinance as yf
from vnstock import Vnstock 



# Outstanding share values
vic_os = 3823.661
vhm_os = 4107.412
vre_os = 2272.318
vfs_os = 2338
vpl_os = 1790

# Parent net debt
vic_net_debt = -96161

# Ownership values
vhm_ownership = 0.735
vre_ownership = 0.188
vfs_ownership = 0.507
vpl_ownership = 0.855
vinschool_ownership = 1
vinmec_ownership = 0.75

# Website title
st.set_page_config(page_title="VIC Valuation", page_icon=":moneybag:", layout="wide")
st.title('App for VIC Valuation')
st.write('Put in the following variables to calculate the valuation of VIC')

# Input for FX
st.title('Input FX Rate')
col_fx1, col_fx2 = st.columns([2, 2])
with col_fx1:
    fx = st.number_input('Enter FX Rate (USD/VND)', step=0.1, value=25800.0)
with col_fx2:
    st.write("")  # spacer for alignment
    st.write("")  # spacer for alignment
    st.write("Rate used for USD to VND conversion")

# VFS auto fetch
st.title('Fetching VFS share price from Yahoo Finance')
vfs_ticker = yf.Ticker("VFS")
vfs_data = vfs_ticker.history(period="1d")
if not vfs_data.empty:
    vfs_yf = vfs_data["Close"].iloc[-1]
    st.success(f"Pulled latest VFS price: ${vfs_yf:.2f} from Yahoo Finance")
else:
    vfs_yf = 3.72  # fallback in case data pull fails
    st.error("Failed to fetch VFS price from Yahoo Finance.")

# VIC/VHM/VRE auto fetch
st.title('Fetching VIC/VHM/VRE share prices from VNSTOCK')
# Set up pulling live data from VNSTOCK
current_price = []
for symbol in ['VIC', 'VHM', 'VRE']:
    stock = Vnstock().stock(symbol=symbol, source='VCI')
    df = stock.quote.history(start='2025-05-01', interval='1D')
    current_price.append(df['close'].iloc[-1])
# Assigning the current price to variables
vic_price = current_price[0]
vhm_price = current_price[1]
vre_price = current_price[2]
if vic_price and vhm_price and vre_price:
    st.success(f"Pulled latest prices: VIC: {vic_price:.1f}, VHM: {vhm_price:.1f}, VRE: {vre_price:.1f} from VNSTOCK")


# UI for multiple share prices and private valuations
st.title('Input share prices and private valuations')
# Input definitions: (label, default, step, ownership)
input_fields = [
    ("VHM Share Price (VNDk)", vhm_price, 0.1, vhm_ownership),
    ("VRE Share Price (VNDk)", vre_price, 0.1, vre_ownership),
    ("VSF Share Price (USD) - defaulted live price", vfs_yf, 0.01, vfs_ownership),
    ("VPL Share Price (VNDk)", 71.0, 0.1, vpl_ownership),
    ("Vinschool Valuation (USDbn)", 1.0, 0.1, vinschool_ownership),
    ("Vinmec Valuation (USDbn)", 0.8, 0.1, vinmec_ownership),
]
# Store inputs
inputs = []

for label, default, step, ownership in input_fields:
    col1, col2 = st.columns([2, 2])
    with col1:
        value = st.number_input(label, step=step, value=default)
    with col2:
        st.write("")  # spacer for alignment
        st.write("")  # spacer for alignment
        st.write(f"Ownership: {ownership * 100:.1f}%")
    inputs.append(value)

# Unpack into variables
vhm, vre, vfs, vpl, vinschool, vinmec = inputs

# Function to calculate VIC valuation
def vic_valuation(vhm, vre, vfs, vpl, vinschool, vinmec):
    vhm_value = vhm * vhm_os * vhm_ownership
    vre_value = vre * vre_os * vre_ownership
    vfs_value = (vfs * vfs_os * vfs_ownership) * (fx / 1000)
    vpl_value = vpl * vpl_os * vpl_ownership
    vinschool_value = vinschool * vinschool_ownership * fx 
    vinmec_value = vinmec * vinmec_ownership * fx 

    total_value = vhm_value + vre_value + vfs_value + vpl_value + vinschool_value + vinmec_value + vic_net_debt
    value_per_share = total_value / vic_os 
    return value_per_share

button1 = st.button('Calculate VIC Valuation')
if button1:
    result = vic_valuation(vhm, vre, vfs, vpl, vinschool, vinmec)
    st.markdown(
        f"<h2 style='color:#2E8B57;'>📈 VIC Valuation/Share: <strong>{result * 1000:,.0f} VND</strong></h2>",
        unsafe_allow_html=True
    )
