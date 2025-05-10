#%%
import streamlit as st
import yfinance as yf

# Outstanding share values
vic_os = 3823.661
vhm_os = 4107.412
vre_os = 2272.318
vfs_os = 2338
vpl_os = 1790

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

# UI for multiple share prices and private valuations
st.title('Input share prices and private valuations')
# Input definitions: (label, default, step, ownership)
input_fields = [
    ("VHM Share Price (VNDk)", 62.0, 0.1, vhm_ownership),
    ("VRE Share Price (VNDk)", 25.0, 0.1, vre_ownership),
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

    total_value = vhm_value + vre_value + vfs_value + vpl_value + vinschool_value + vinmec_value
    value_per_share = total_value / vic_os 
    return value_per_share

button1 = st.button('Calculate VIC Valuation')
if button1:
    result = vic_valuation(vhm, vre, vfs, vpl, vinschool, vinmec)
    st.markdown(
        f"<h2 style='color:#2E8B57;'>📈 VIC Valuation/Share: <strong>{result * 1000:,.0f} VND</strong></h2>",
        unsafe_allow_html=True
    )
