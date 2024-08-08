import streamlit as st
from handcalcs.decorator import handcalc
import handcalcs
from math import pi, sqrt, ceil

ARAH_X = "long"
ARAH_Y = "trans"

### INPUT SIDEBAR -----------------------------------------------------------------------------------------------------------------------------------------------#
with st.sidebar:
    ### INPUT INFORMASI PROYEK ----------------------------------------------------------------------------------------------------------------------------------#
    st.markdown("# Informasi Proyek")
    project = st.text_input("Nama Proyek",
                            value="-")
    document_code = st.text_input("Kode Dokumen",
                                  help="Apabila tidak ada inputkan tanda - ",
                                  value="-")
    date = st.date_input("Tanggal Dibuat",
                         help="Masukan Tanggal")
    pier_number = st.text_input("Nomor Pier",
                             help="Masukan Type Struktur",
                             value="-")
    ### INPUT PARAMETER -----------------------------------------------------------------------------------------------------------------------------------------#
    st.markdown("# Umum")
    zona_geser = st.radio("Zona Geser",
                        ["Sendi Plastis","Luar Sendi Plastis"]
                        )
    st.markdown("# Parameter")
    st.markdown("## Material")
    compression_strength_of_concrete = st.number_input("Kuat Tekan Beton, $f_c$ (MPa)",
                                                       help="Masukan nilai kuat tekan beton $f_c$",
                                                       value=35)
    rebar_yield_strength = st.number_input("Kuat Leleh Tulangan, $f_y$ (MPa)",
                                           help="Masukan kuat leleh tulangan $f_y$",
                                           value=420)
    
    st.markdown("## Gaya")
    shear_force_design_X = st.number_input("Gaya Geser Arah X  (kN)",
                                        help="Gaya rencana untuk kolom diambil nilai terkecil dari yang ditentukan pada  Pasal 5.9.3.1 SNI:2833-2016 yaitu Nilai terkecil berdasarkan desain elastis dengan kombinasi beban gempa dan menggunakan faktor R sama dengan 1 untuk kolom atau nilai berdasarkan analisis sendi plastis.",
                                        value=1000)
    shear_force_design_Y = st.number_input("Gaya Geser Arah Y (kN)",
                                        help="Gaya rencana untuk kolom diambil nilai terkecil dari yang ditentukan pada  Pasal 5.9.3.1 SNI:2833-2016 yaitu Nilai terkecil berdasarkan desain elastis dengan kombinasi beban gempa dan menggunakan faktor R sama dengan 1 untuk kolom atau nilai berdasarkan analisis sendi plastis.",
                                        value=2000)
    axial_force_design = st.number_input("Gaya Axial",
                                         help="Gaya axial yang terjadi yang konkuren dengan gaya geser yang terjadi",
                                         value=1000)
    
    st.markdown("## Penampang")
    column_length = st.number_input("Panjang Pier (mm)",
                                    help="Panjang penampang pier (mm)",
                                    value=2000)
    column_width = st.number_input("Lebar Pier (mm)",
                                   help="Lebar penampang pier (mm)",
                                   value=1500)
    column_height = st.number_input("Tinggi Pier (mm)",
                                    help="Tinggi pier (mm)",
                                    value=7000)
    cover_rebar = st.number_input("Cover Beton (mm)",
                                  help="Masukan selimut beton",
                                  value=50)
    
    st.markdown("## Konfigurasi Tulangan")
    shear_rebar_spacing = st.number_input("Spasi Tulangan Geser (mm)",
                                          value=100)
    shear_rebar_diameter = st.number_input("Diameter Tulangan Sengkang (mm)",
                                           value=19)
    shear_rebar_ratio_X = st.number_input("Rasio Tulangan Geser Pier Wall Arah X",
                                        help="Rasio Tulangan Geser untuk type dinding, ratio minimum 0.0018",
                                        value=0.002,
                                        step=0.001,
                                        format="%.4f")
    shear_rebar_ratio_Y = st.number_input("Rasio Tulangan Geser Pier Wall Arah Y",
                                        help="Rasio Tulangan Geser untuk type dinding, ratio minimum 0.0018",
                                        value=0.002,
                                        step=0.001,
                                        format="%.4f")
    st.markdown("## Faktor Reduksi")
    shear_reduction_factor = st.number_input("Faktor Reduksi Kapasitas Geser",
                                             help="0.75 untuk geser",
                                             value=0.75,
                                             )
### PARAMETER UNTUK ANALISIS -------------------------------------------------------------------------------------------------------------------------------------#

f_c = compression_strength_of_concrete
f_y = rebar_yield_strength
L=column_length
B=column_width
H=column_height
A_g = L*B
A_e = 0.8*A_g
P_c = (L+B)*2
c=cover_rebar
S_v=shear_rebar_spacing
D_v=shear_rebar_diameter
rho_x=shear_rebar_ratio_X
rho_y=shear_rebar_ratio_Y
phi_V = shear_reduction_factor
V_u_x = shear_force_design_X*1000
V_u_y = shear_force_design_Y*1000
P_u = axial_force_design*1000
beta = 2
h_x = B-2*c
h_y = L-2*c
A_c = h_x*h_y

### LATEX HANDCALCS EQUATION -------------------------------------------------------------------------------------------------------------------------------------#
#### PENGECEKAN PERSYARATAN KOLOM #

@handcalc(override="long",precision=2)
def x_pier_column_check():
    Ratio_x = H/L
    return Ratio_x
ratio_pier_x_column_latex,ratio_pier_x_column=x_pier_column_check()

@handcalc(override="long",precision=2)
def y_pier_column_check():
    Ratio_y = H/B
    return Ratio_y
ratio_pier_y_column_latex,ratio_pier_y_column=y_pier_column_check()

#### ANALISIS KEBUTUHAN KAPASITAS GESER BETON --------------------------------------------------------------------------------------------------------------------#

@handcalc(override="long",precision=2)
def d_v_arah_x():
    d_v_x = L-c
    return d_v_x
d_v_x_latex,d_v_x = d_v_arah_x()

@handcalc(override="long",precision=2)
def d_v_arah_y():
    d_v_y = B-c
    return d_v_y
d_v_y_latex,d_v_y = d_v_arah_y()


@handcalc(override="long",precision=2)
def shear_concrete_capacity_reduction():
    phi_V_c = P_u/((A_g*f_c*0.1))
    return phi_V_c
if P_u > (0.1*A_g*f_c):
    phi_V_c = 1
elif P_u < (0.1*A_g*f_c):
    phi_V_c_latex,phi_V_c = shear_concrete_capacity_reduction()


@handcalc(override="long",precision=2)
def shear_concrete_capacity_x():
    V_c_x = 0.083*beta*sqrt(f_c)*B*d_v_x*phi_V_c
    return V_c_x
V_c_x_latex,V_c_x = shear_concrete_capacity_x()

@handcalc(override="long",precision=2)
def shear_concrete_capacity_y():
    V_c_y = 0.083*beta*sqrt(f_c)*L*d_v_y*phi_V_c
    return V_c_y
V_c_y_latex,V_c_y = shear_concrete_capacity_y()

#### ANALISIS KEBUTUHAN TULANGAN GESER
@handcalc(override="long",precision=2)
def shear_steel_capacity_x():
    V_s_x = (V_u_x/phi_V)-V_c_x
    return V_s_x
#V_s_x_latex,V_s_x=shear_steel_capacity_x()
if V_c_x < V_u_x/phi_V:
    V_s_x_latex,V_s_x=shear_steel_capacity_x()
elif V_c_x > V_u_x/phi_V:
    V_s_x_latex,V_s_x="V_{s_x} = 0",0

@handcalc(override="long",precision=2)
def shear_steel_capacity_y():
    V_s_y = (V_u_y/phi_V)-V_c_y
    return V_s_y
#V_s_y_latex,V_s_y=shear_steel_capacity_y()
if V_c_y < V_u_y/phi_V:
    V_s_y_latex,V_s_y=shear_steel_capacity_y()
elif V_c_y > V_u_y/phi_V:
    V_s_y_latex,V_s_y="V_{s_y} = 0",0

@handcalc(override="long",precision=2)
def shear_capacity_max():
    V_s_max = 0.67*sqrt(f_c)*A_e
    return V_s_max
V_s_max_latex,V_s_max=shear_capacity_max()

@handcalc(override="long",precision=2)
def shear_rebar_req_x():
    A_v_x = (V_s_x*S_v)/(f_y*d_v_x)
    return A_v_x

@handcalc(override="long",precision=4)
def shear_rebar_req_wall_x():
    A_v_x = (B*H)*rho_x
    return A_v_x

#A_v_x_latex,A_v_x=shear_rebar_req_x()
if ratio_pier_x_column > 2.5:
    if V_c_x < V_u_x/phi_V:
        A_v_x_latex,A_v_x=shear_rebar_req_x()
    elif V_c_x > V_u_x/phi_V:
        A_v_x_latex,A_v_x="A_{v_x} = 0",0
elif ratio_pier_x_column < 2.5:
    A_v_x_latex,A_v_x=shear_rebar_req_wall_x()


@handcalc(override="long",precision=2)
def shear_rebar_req_y():
    A_v_y = (V_s_y*S_v)/(f_y*d_v_y)
    return A_v_y

@handcalc(override="long",precision=4)
def shear_rebar_req_wall_y():
    A_v_y = (L*H)*rho_y
    return A_v_y

#A_v_y_latex,A_v_y=shear_rebar_req_y()
if ratio_pier_y_column > 2.5:
    if V_c_y < V_u_y/phi_V:
        A_v_y_latex,A_v_y=shear_rebar_req_y()
    elif V_c_y > V_u_y/phi_V:
        A_v_y_latex,A_v_y="A_{v_y} = 0",0
elif ratio_pier_y_column < 2.5:
    A_v_y_latex,A_v_y=shear_rebar_req_wall_y()

#### TULANGAN GESER MINIMUM ----------------------

@handcalc(override="long",precision=2)
def shear_rebar_min_x():
    A_v_min_x = 0.083*sqrt(f_c)*((B*S_v)/f_y)
    return A_v_min_x
A_v_min_x_latex,A_v_min_x=shear_rebar_min_x()

@handcalc(override="long",precision=2)
def shear_rebar_min_y():
    A_v_min_y = 0.083*sqrt(f_c)*((L*S_v)/f_y)
    return A_v_min_y
A_v_min_y_latex,A_v_min_y=shear_rebar_min_y()

#### SPASI TULANGAN GESER MAX
def spacing_max():
    Vsx_check=(1/3)*sqrt(f_c)*B*d_v_x
    Vsy_check=(1/3)*sqrt(f_c)*L*d_v_y
    if V_s_x < Vsx_check:
        S_max_x = min(d_v_x/2,600)
    elif V_s_x > Vsx_check:
        S_max_x = min(d_v_x/2,300)
    if V_s_y < Vsy_check:
        S_max_y = min(d_v_y/2,600)
    elif V_s_y > Vsy_check:
        S_max_y = min(d_v_y/2,300)
    S_max = min(S_max_x,S_max_y)
    return S_max

if zona_geser == "Sendi Plastis":
    S_max = 100
if zona_geser == "Luar Sendi Plastis":
    S_max = spacing_max()

#### KAPASITAS PENAMPANG
@handcalc(override="long",precision=2)
def section_capacity_x():
    V_n_x = V_c_x +V_s_x
    V_r_x = phi_V*V_n_x
    return round(V_r_x)

@handcalc(override="long",precision=4)
def section_capacity_wall_x():
    V_n_x = (0.165*sqrt(f_c)+rho_x*f_y)*B*d_v_x
    V_r_x_1= 0.665*sqrt(f_c)*B*d_v_x
    V_r_x_2= phi_V*V_n_x
    V_r_x = min(V_r_x_1,V_r_x_2)
    return round(V_r_x)

if ratio_pier_x_column > 2.5:
    V_r_x_latex,V_r_x = section_capacity_x()
elif ratio_pier_x_column < 2.5:
    V_r_x_latex,V_r_x = section_capacity_wall_x()

@handcalc(override="long",precision=2)
def section_capacity_y():
    V_n_y = V_c_y +V_s_y
    V_r_y = phi_V*V_n_y
    return round(V_r_y)

@handcalc(override="long",precision=4)
def section_capacity_wall_y():
    V_n_y = (0.165*sqrt(f_c)+rho_y*f_y)*L*d_v_y
    V_r_y_1= 0.665*sqrt(f_c)*L*d_v_y
    V_r_y_2= phi_V*V_n_y
    V_r_y = min(V_r_y_1,V_r_y_2)
    return round(V_r_y)

if ratio_pier_y_column > 2.5:
    V_r_y_latex,V_r_y = section_capacity_y()
elif ratio_pier_y_column < 2.5:
    V_r_y_latex,V_r_y = section_capacity_wall_y()
#### TULANGAN CONFINEMENT
@handcalc(override="long",precision=2)
def confinement_rebar_x():
    A_sh_1 = 0.3*S_v*h_x*(f_c/f_y)*(A_g/A_c-1)
    A_sh_2 = 0.12*S_v*h_x*f_c/f_y
    A_sh_x = max(A_sh_1,A_sh_2)
    return A_sh_x
A_sh_x_latex,A_sh_x=confinement_rebar_x()

@handcalc(override="long",precision=2)
def confinement_rebar_y():
    A_sh_1 = 0.3*S_v*h_y*(f_c/f_y)*(A_g/A_c-1)
    A_sh_2 = 0.12*S_v*h_y*f_c/f_y
    A_sh_y = max(A_sh_1,A_sh_2)
    return A_sh_y
A_sh_y_latex,A_sh_y=confinement_rebar_y()
### MARKDOWN & TEX -----------------------------------------------------------------------------------------------------------------------------------------------------#

MD_PARAMETER_MATERIAL = f"""
- Kuat tekan beton, $f_c = {f_c} \ MPa$
- Kuat leleh tulangan, $f_y = {f_y} \ MPa$
"""
MD_PARAMETER_PENAMPANG = f"""
- Panjang pier, $L = {L} \ mm$
- Lebar pier, $B = {B} \ mm$
- Tinggi pier, $H = {H} \ mm$
- Luas penampang, $A_g = {A_g} \ mm^{{2}}$
- Luas penampang efektif, $A_e = {A_e} \ mm^{{2}}$
- Perimeter penampang, $P_c = {P_c} \ mm$
- Cover beton, $c = {c} \ mm$
"""

MD_PARAMETER_TULANGAN = f"""
- Spasi tulangan geser, $S_v = {S_v} \ mm$
"""

MD_PARAMETER_GAYA = f"""
- Gaya geser ultimate,$V_{{u_x}} = {V_u_x/1000} \ kN \Rightarrow  {V_u_x} \ N$
- Gaya geser ultimate,$V_{{u_y}} = {V_u_y/1000} \ kN \Rightarrow  {V_u_y} \ N$
- Gaya axial ultimate,$P_u = {P_u/1000} \ kN \Rightarrow  {P_u} \ N$
"""
MD_PARAMETER_CONFINEMENT = f"""
- Panjang core beton arah x, $h_x = {h_x} \ mm$
- Panjang core beton arah y, $h_y = {h_y} \ mm$
- Luas core beton, $A_c = {A_c} \ mm^{{2}}$
"""

### BODY WEB -----------------------------------------------------------------------------------------------------------------------------------------------------#
st.title("TIA Engineering")
st.subheader("Aplikasi Analisis Kebutuhan Tulangan Geser Pier")
st.markdown("Analisis tulangan pada aplikasi ini dihitung berdasarkan Peraturan/Code dan Referensi Sebagai Berikut :")
st.markdown("""
            - **SNI 2833:2016** tentang Perencanaan Jembatan Terhadap Beban Gempa
            - **RSNI T-12-2004** tentang Perencanaan Struktur Beton untuk Jembatan
            - **SE Dirjen Bina Marga No.06/SE/Db/2021** tentang Panduan Praktis Perencanaan Teknis Jembatan
            """)
st.divider()
st.markdown("## Informasi Proyek")
col_IP1,col_IP2=st.columns(2)
with col_IP1:
    st.markdown(f"**Proyek : {project}**")
    st.markdown(f"**Nomor Pier : {pier_number}**")
with col_IP2:
    st.markdown(f"**Kode Dokumen : {document_code}**")
    st.markdown(f"**Tanggal : {date}**")
st.markdown("## Parameter")
st.image('notasigaya.png',caption="Notasi Arah Gaya")
st.markdown("### Material")
st.markdown(MD_PARAMETER_MATERIAL)
st.markdown("### Penampang")
st.markdown(MD_PARAMETER_PENAMPANG)
if zona_geser == "Sendi Plastis":
    st.markdown(MD_PARAMETER_CONFINEMENT)
st.markdown("### Tulangan")
st.markdown(MD_PARAMETER_TULANGAN)
if ratio_pier_x_column < 2.5:
    st.markdown(f"""
                - Rasio tulangan horizontal penampang arah {ARAH_X}, $ \Rho_x = {rho_x}$
                - Rasio tulangan horizontal penampang arah {ARAH_Y}, $ \Rho_y = {rho_y}$
""")
st.markdown("### Gaya")
st.markdown(MD_PARAMETER_GAYA)
with st.expander("Lihat Penjelasan Gaya Geser Ultimate"):
    if zona_geser == "Sendi Plastis":
        st.markdown("Gaya rencana untuk kolom diambil nilai terkecil dari yang ditentukan pada **Pasal 5.9.3.1 SNI:2833-2016** yaitu Nilai terkecil berdasarkan desain elastis dengan kombinasi beban gempa dan menggunakan faktor R sama dengan 1 untuk kolom atau nilai berdasarkan analisis sendi plastis.")
    if zona_geser == "Luar Sendi Plastis":
        st.markdown("Gaya rencana untuk kolom diambil gaya geser terfaktor")
st.markdown("## Perhitungan")
## CEK PERSYARATAN KOLOM
st.markdown("### Cek persyaratan kolom $H/L > 2.5$ :")
with st.expander("Lihat Penjelasan"):
    st.markdown("Pendukung vertikal harus dianggap sebagai kolom jika rasio tinggi bersih terhadap dimensi maksimum penampangnya lebih besar dari 2,5. Untuk kolom dengan pembesaran, dimensi rencana maksimum diambil pada bagian minimum dari penampangnya. Untuk pendukung dengan rasio kurang dari 2,5 maka ketentuan untuk pilar dinding **Pasal 7.4.2 SNI:2833-2016** dapat digunakan.")
col_A1,col_A2 = st.columns(2)
def column_A(arah,ratio_pier_column_latex,ratio_pier_column,length): #<- FUNGSI KOLOM A
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        st.latex(ratio_pier_column_latex)
        if ratio_pier_column > 2.5:
            st.info(f"Rasio $H/{length}= {round(ratio_pier_column,2)}> 2.5$ Persyaratan kolom terpenuhi")
        if ratio_pier_column < 2.5:
            st.warning(f"Rasio $H/{length}= {round(ratio_pier_column,2)}< 2.5$ Gunakan analisis pilar dinding")

with col_A1:
    column_A(ARAH_X,ratio_pier_x_column_latex,ratio_pier_x_column,"L")
with col_A2:
    column_A(ARAH_X,ratio_pier_y_column_latex,ratio_pier_y_column,"B")
### CEK KEBUTUHAN TULANGAN GESER -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("### Analisis Kebutuhan Tulangan Geser")
st.markdown(f"- Tinggi bidang geser efektif, $d_v$ :")
col_B1,col_B2 = st.columns(2)
with col_B1:
    with st.container(border=True):
        st.markdown(f"**Arah {ARAH_X}**")
        st.latex(d_v_x_latex)
        st.info(f" - $d_{{v_{{{ARAH_X}}}}} = {d_v_x} \ mm$")

with col_B2:
    with st.container(border=True):
        st.markdown(f"**Arah {ARAH_Y}**")
        st.latex(d_v_y_latex)
        st.info(f" - $d_{{v_{{{ARAH_Y}}}}} = {d_v_y} \ mm$")

st.markdown(f"- Faktor indikasi, $\\beta = {beta}$")
### CEK AXIAL -------------------------------------------------------
st.markdown(f"- Cek apakah $P_u > 0.1 A_g f_c$ :")
with st.expander("Lihat Penjelasan"):
    st.markdown("Untuk gaya tekan kurang dari $0.1 A_g f_c$, $Vc$ diambil nilai yang turun secara linier dari nilai pada **Persamaan 20 SNI:2833-2016** hingga nol pada gaya tekan sama dengan nol.")
if P_u > (0.1*A_g*f_c):
    st.info(f"$P_u={P_u/1000}\ kN > 0.1 A_g f_c = {(0.1*A_g*f_c)/1000} \ kN$ Kapasitas geser beton $V_c$ utuh")
    st.markdown(f"- Faktor reduksi kapasitas geser beton, $\Phi_{{V_c}}={phi_V_c}$")

elif P_u < (0.1*A_g*f_c):
    st.warning(f"$P_u={P_u/1000}\ kN < 0.1 A_g f_c = {(0.1*A_g*f_c)/1000} \ kN$ Kapasitas geser beton $V_c$ direduksi")
    st.markdown(f"- Faktor reduksi kapasitas geser beton :")
    st.latex(phi_V_c_latex)
### CEK KAPASITAS GESER BETON --------------------------------------------------
st.markdown(f"- Kapasitas geser beton,$V_c$ :")
def column_C(arah,V_c_latex,V_c):
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        st.latex(V_c_latex)
        st.info(f" - $V_{{c_{{{arah}}}}} = {round(V_c/1000)} \ kN$")

col_C1,col_C2 = st.columns(2)
with col_C1:
    if ratio_pier_x_column > 2.5:
        column_C(ARAH_X,V_c_x_latex,V_c_x)
    elif ratio_pier_x_column < 2.5:
        with st.container(border=True):
            st.markdown(f"**Arah {ARAH_X}**")
            st.info("Nilai $V_c$ tidak dihitung untuk analisis pilar dinding")
with col_C2:
    if ratio_pier_y_column > 2.5:
        column_C(ARAH_Y,V_c_y_latex,V_c_y)
    elif ratio_pier_y_column < 2.5:
        with st.container(border=True):
            st.markdown(f"**Arah {ARAH_Y}**")
            st.info("Nilai $V_c$ tidak dihitung untuk analisis pilar dinding")

#### ANALISIS KEBUTUHAN TULANGAN GESER -----------------------------------------------------------------------------------------------------
st.markdown("- Kapasitas geser tulangan, $V_s$ :")
def column_D(arah,V_s_latex,V_s):
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        st.latex(V_s_latex)
        st.info(f"$V_{{s_{{{arah}}}}} = {round(V_s/1000)} \ kN$")

col_D1,col_D2 = st.columns(2)
with col_D1:
    if ratio_pier_x_column > 2.5:
        column_D(ARAH_X,V_s_x_latex,V_s_x)
    elif ratio_pier_x_column < 2.5:
        with st.container(border=True):
            st.markdown(f"**Arah {ARAH_X}**")
            st.info("Nilai $V_s$ tidak dihitung untuk analisis pilar dinding")
with col_D2:
    if ratio_pier_y_column > 2.5:
        column_D(ARAH_Y,V_s_y_latex,V_s_y)
    elif ratio_pier_y_column < 2.5:
        with st.container(border=True):
            st.markdown(f"**Arah {ARAH_Y}**")
            st.info("Nilai $V_s$ tidak dihitung untuk analisis pilar dinding")

st.markdown("- Cek nilai $V_s$ tidak boleh melebihi $0.67 \sqrt{f_c} A_e $ :")
st.latex(V_s_max_latex)
st.info(f"$V_{{s_{{max}}}}={round(V_s_max/1000)} \ kN$")

def column_E(arah,V_s):
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        if V_s < V_s_max:
            st.success(f"$V_{{s_{{{arah}}}}}$ < $V_{{s_{{max}}}}$ OK !")
        elif V_s > V_s_max:
            st.error(f"$V_{{s_{{{arah}}}}}$ > $V_{{s_{{max}}}}$ PENAMPANG KURANG !")
        
col_E1,col_E2 = st.columns(2)
with col_E1:
    if ratio_pier_x_column > 2.5:
        column_E(ARAH_X,V_s_x)
    elif ratio_pier_x_column < 2.5:
        with st.container(border=True):
            st.markdown(f"**Arah {ARAH_X}**")
            st.info("Tidak di cek untuk analisis pilar dinding")
with col_E2:
    if ratio_pier_y_column > 2.5:
        column_E(ARAH_Y,V_s_y)
    elif ratio_pier_y_column < 2.5:
        with st.container(border=True):
            st.markdown(f"**Arah {ARAH_Y}**")
            st.info("Tidak di cek untuk analisis pilar dinding")

st.markdown("- Luas kebutuhan tulangan, $A_v$ :")
def column_F(arah,A_v_latex,A_v):
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        st.latex(A_v_latex)
        st.info(f"$A_{{v_{{{arah}}}}} = {round(A_v)} \ mm^{{2}}$")

col_F1,col_F2 = st.columns(2)
with col_F1:
    column_F(ARAH_X,A_v_x_latex,A_v_x)
with col_F2:
    column_F(ARAH_Y,A_v_y_latex,A_v_y)

st.markdown("- Luas tulangangan minimum, $A_{v_{min}}$ :")
def column_G(arah,A_v_min_latex,A_v_min):
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        st.latex(A_v_min_latex)
        st.info(f"$A_{{v_{{min_{{{ARAH_X}}}}}}} = {round(A_v_min)} \ mm^{{2}}$")
col_G1,col_G2 = st.columns(2)
with col_G1:
    column_G(ARAH_X,A_v_min_x_latex,A_v_min_x)
with col_G2:
    column_G(ARAH_Y,A_v_min_y_latex,A_v_min_y)

st.markdown("- Cek spasi tulangan maksimum, $S_{max}$ :")
st.info(f"$S_{{max}} = {S_max} \ mm$")
if S_v > S_max:
     st.error("$S_v > S_{max}$ NOT OK")
elif S_v <= S_max:
    st.success("$S_v \leq S_{max}$ OK")

st.markdown("- Kapasitas Penampang, $V_r = \phi_v V_n$ :")
def column_H(arah,V_r_latex,V_r,V_u):
    with st.container(border=True):
        st.markdown(f"**Arah {arah}**")
        st.latex(V_r_latex)
        if V_r >= V_u:
            st.success(f"$V_r = {(V_r/1000)} \ kN \geq {V_u/1000} \ kN$")
        elif V_r <= V_u:
            st.error(f"$V_r = {(V_r/1000)} \ kN \leq {V_u/1000} \ kN$")
    
col_H1,col_H2 = st.columns(2)
with col_H1:
    column_H(ARAH_X,V_r_x_latex,V_r_x,V_u_x)
with col_H2:
    column_H(ARAH_Y,V_r_y_latex,V_r_y,V_u_y)

if zona_geser == "Sendi Plastis":
    st.markdown("### Analisis Kebutuhan Tulangan Confinement")
    def column_I(arah,A_sh_latex,A_sh):
        with st.container(border=True):
            st.markdown(f"**Arah {arah}**")
            st.latex(A_sh_latex)
            st.info(f"$A_{{sh_{{{arah}}}}} = {round(A_sh)} \ mm^{{2}}$")

    col_I1,col_I2 = st.columns(2)
    with col_I1:
        column_I(ARAH_X,A_sh_x_latex,A_sh_x)
    with col_I2:
        column_I(ARAH_Y,A_sh_y_latex,A_sh_y)

st.markdown("### Resume Tulangan")
luas_tulangan_pier_wall_X = (A_v_x)/(H/S_v)
luas_tulangan_pier_wall_Y = (A_v_y)/(H/S_v)
def jumlah_tulangan_pier(A_v,A_v_min,A_sh):
    if zona_geser == "Sendi Plastis":
        N_v=max(A_v,A_v_min,A_sh)/(0.25*pi*D_v**2)
    if zona_geser == "Luar Sendi Plastis":
        N_v=max(A_v,A_v_min)/(0.25*pi*D_v**2)
    return N_v

def jumlah_tulangan_pier_wall(A_v_wall,A_v_min,A_sh):
    if zona_geser == "Sendi Plastis":
        N_v=max(A_v_wall,A_v_min,A_sh)/(0.25*pi*D_v**2)
    if zona_geser == "Luar Sendi Plastis":
        N_v=max(A_v_wall,A_v_min)/(0.25*pi*D_v**2)
    return N_v

jumlah_tulangan_pier_X= jumlah_tulangan_pier(A_v_x,A_v_min_x,A_sh_x)
jumlah_tulangan_pier_Y= jumlah_tulangan_pier(A_v_y,A_v_min_y,A_sh_y)
jumlah_tulangan_pier_wall_X=jumlah_tulangan_pier_wall(luas_tulangan_pier_wall_X,A_v_min_x,A_sh_x)
jumlah_tulangan_pier_wall_Y=jumlah_tulangan_pier_wall(luas_tulangan_pier_wall_Y,A_v_min_y,A_sh_y)

st.markdown("Dari hasil analisis dapat disimpulkan tulangan geser yang harus dipasang adalah sebagai berikut :")
def MD_RESUME_PIER(arah,ratio_pier_column,A_v,A_v_min,A_sh,jumlah_tulangan_pier,luas_tulangan_pier_wall,jumlah_tulangan_pier_wall):
    if ratio_pier_column > 2.5: # KALAU PIER KOLOM
        if zona_geser == "Sendi Plastis": 
            st.markdown(f"""
            - Kebutuhan tulangan geser {arah} adalah **{round(A_v)} mm2** 
            - Kebutuhan luas tulangan minimum {arah} adalah **{round(A_v_min)} mm2**
            - Kebutuhan luas tulangan confinement {arah} adalah **{round(A_sh)} mm2**
            - Maka luas tulangan yang harus dipasang arah {arah} adalah **{round(max(A_v,A_v_min,A_sh))} mm2**
            - Konfigurasi yang digunakan adalah **{ceil(jumlah_tulangan_pier)}D{D_v}-{S_v}**
            """)
        if zona_geser == "Luar Sendi Plastis":
            st.markdown(f"""
            - Kebutuhan tulangan geser {arah} adalah **{round(A_v)} mm2** 
            - Kebutuhan luas tulangan minimum {arah} adalah **{round(A_v_min)} mm2**
            - Maka luas tulangan yang harus dipasang arah {arah} adalah **{round(max(A_v,A_v_min))} mm2**
            - Konfigurasi yang digunakan adalah **{ceil(jumlah_tulangan_pier)}D{D_v}-{S_v}**
            """)
    elif ratio_pier_column < 2.5: # KALAU PIER WALL
        if zona_geser == "Sendi Plastis":
            st.markdown(f"""
            - Kebutuhan tulangan geser {arah} setelah di bagi dengan spasi adalah **{round(luas_tulangan_pier_wall)} mm2** 
            - Kebutuhan luas tulangan minimum {arah} adalah **{round(A_v_min)} mm2**
            - Kebutuhan luas tulangan confinement {arah} adalah **{round(A_sh)} mm2**
            - Maka luas tulangan yang harus dipasang arah {arah} adalah **{round(max(luas_tulangan_pier_wall,A_v_min,A_sh))} mm2**
            - Konfigurasi yang digunakan adalah **{ceil(jumlah_tulangan_pier_wall)}D{D_v}-{S_v}**
            """)
        if zona_geser == "Luar Sendi Plastis":
            st.markdown(f"""
            - Kebutuhan tulangan geser {arah} adalah **{round(luas_tulangan_pier_wall)} mm2** 
            - Kebutuhan luas tulangan minimum {arah} adalah **{round(A_v_min)} mm2**
            - Maka luas tulangan yang harus dipasang arah {arah} adalah **{round(max(luas_tulangan_pier_wall,A_v_min))} mm2**
            - Konfigurasi yang digunakan adalah **{ceil(jumlah_tulangan_pier_wall)}D{D_v}-{S_v}**
            """)




col_J1,col_J2 = st.columns(2)
with col_J1:
    with st.container(border=True):
        st.markdown(f"**Arah {ARAH_X}**")
        MD_RESUME_PIER(ARAH_X,ratio_pier_x_column,A_v_x,A_v_min_x,A_sh_x,jumlah_tulangan_pier_X,luas_tulangan_pier_wall_X,jumlah_tulangan_pier_wall_X) 
with col_J2:
    with st.container(border=True):
        st.markdown(f"**Arah {ARAH_Y}**")
        MD_RESUME_PIER(ARAH_Y,ratio_pier_y_column,A_v_y,A_v_min_y,A_sh_y,jumlah_tulangan_pier_Y,luas_tulangan_pier_wall_Y,jumlah_tulangan_pier_wall_Y)