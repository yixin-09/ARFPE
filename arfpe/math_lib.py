from mpmath import *
import numpy as np
from pygsl.testing import sf
mp.dps = 60
#gsl_sf_clausen_e 1
rf0 = lambda x: clsin(2,x)


#gsl_sf_laguerre_1_e 2
rf1 = lambda x,y: fadd(1.0,fsub(x,y,exact=True),exact=True)


#gsl_sf_laguerre_2_e 2
rf2 = lambda x,y: laguerre(2, x, y)


#gsl_sf_laguerre_3_e 2
rf3 = lambda x,y: laguerre(3, x, y)


#gsl_sf_multiply_e 2
rf4 = lambda x,y: fmul(x,y,exact=True)


#gsl_sf_dilog_e 1
rf5 = lambda x: polylog(2,x)


#gsl_sf_bessel_I0_e 1
rf6 = lambda x: besseli(0,x)


#gsl_sf_bessel_I0_scaled_e 1
rf7 = lambda x: fmul(besseli(0,x),exp(-fabs(x)),exact=True)


#gsl_sf_bessel_I1_e 1
rf8 = lambda x: besseli(1,x)


#gsl_sf_bessel_I1_scaled_e 1
rf9 = lambda x: fmul(besseli(1,x),exp(-fabs(x)),exact=True)


#gsl_sf_bessel_Inu_e 2
rf10 = lambda x,y: besseli(x,y)


#gsl_sf_bessel_Inu_scaled_e 2
rf11 = lambda x,y: fmul(besseli(x,y),exp(-y),exact=True)


#gsl_sf_bessel_J0_e 1
rf12 = lambda x: besselj(0,x)


#gsl_sf_bessel_J1_e 1
rf13 = lambda x: besselj(1,x)


#gsl_sf_bessel_Jnu_e 2
rf14 = lambda x,y: besselj(x,y)


#gsl_sf_bessel_K0_e 1
rf15 = lambda x: besselk(0,x)


#gsl_sf_bessel_K0_scaled_e 1
rf16 = lambda x: fmul(besselk(0,x),(exp(x)),exact=True) if (x>0) else besselk(0,x)


#gsl_sf_bessel_K1_e 1
rf17 = lambda x: besselk(1,x)


#gsl_sf_bessel_K1_scaled_e 1
rf18 = lambda x: fmul(besselk(1,x),(exp(x)),exact=True) if (x>0) else besselk(1,x)


#gsl_sf_bessel_Knu_e 2
rf19 = lambda x,y: besselk(x,y)


#gsl_sf_bessel_Knu_scaled_e 2
rf20 = lambda x,y: fmul(besselk(x,y),exp(y),exact=True)


#gsl_sf_bessel_Y0_e 1
rf21 = lambda x: bessely(0,x)


#gsl_sf_bessel_Y1_e 1
rf22 = lambda x: bessely(1,x)


#gsl_sf_bessel_Ynu_e 2
rf23 = lambda x,y: bessely(x,y)


#gsl_sf_bessel_i0_scaled_e 1
rf24 = lambda x: re(fmul(exp(-fabs(x)),besseli(0.5,x)/sqrt(2.0*x/pi),exact=True))


#gsl_sf_bessel_i1_scaled_e 1
rf25 = lambda x: re(fmul(exp(-fabs(x)),besseli(1.5,x)/sqrt(2.0*x/pi),exact=True))


#gsl_sf_bessel_i2_scaled_e 1
rf26 = lambda x: re(fmul(exp(-fabs(x)),besseli(2.5,x)/sqrt(2.0*x/pi),exact=True))


#gsl_sf_bessel_j0_e 1
rf27 = lambda x: fmul(sqrt(pi/(2*x)),besselj(0.5,x),exact=True)


#gsl_sf_bessel_j1_e 1
rf28 = lambda x: fmul(sqrt(pi/(2*x)),besselj(1.5,x),exact=True)


#gsl_sf_bessel_j2_e 1
rf29 = lambda x: fmul(sqrt(pi/(2*x)),besselj(2.5,x),exact=True)


#gsl_sf_bessel_k0_scaled_e 1
rf30 = lambda x: fmul(fmul(exp(x),besselk(0.5,x),exact=True),sqrt(pi/(2*x)),exact=True)


#gsl_sf_bessel_k1_scaled_e 1
rf31 = lambda x: fmul(fmul(exp(x),besselk(1.5,x),exact=True),sqrt(pi/(2*x)),exact=True)


#gsl_sf_bessel_k2_scaled_e 1
rf32 = lambda x: fmul(fmul(exp(x),besselk(2.5,x),exact=True),sqrt(pi/(2*x)),exact=True)


#gsl_sf_bessel_lnKnu_e 2
rf33 = lambda x,y: log(besselk(x,y))


#gsl_sf_bessel_y0_e 1
rf34 = lambda x: fmul(sqrt(pi/(2*x)),bessely(0.5,x),exact=True)
# rf34 = lambda x: -cos(x)/x

#gsl_sf_bessel_y1_e 1
rf35 = lambda x: fmul(sqrt(pi/(2*x)),bessely(1.5,x),exact=True)


#gsl_sf_bessel_y2_e 1
rf36 = lambda x: fmul(sqrt(pi/(2*x)),bessely(2.5,x),exact=True)


#gsl_sf_erf_Q_e 1
rf37 = lambda x: erfc(x/sqrt(2.0))/2.0


#gsl_sf_erf_Z_e 1
rf38 = lambda x: exp(-power(x,2.0)/2)/sqrt(2*pi)


#gsl_sf_erf_e 1
rf39 = lambda x: erf(x)

#gsl_sf_erfc_e 1
rf40 = lambda x: erfc(x)


#gsl_sf_hazard_e 1
rf41 = lambda x: fmul(sqrt(2.0/pi),exp(-power(x,2.0)/2.0),exact=True)/erfc(x/sqrt(2.0))


#gsl_sf_log_erfc_e 1
rf42 = lambda x: log(erfc(x))

#gsl_sf_lambert_W0_e 1
rf43 = lambda x: lambertw(x)

#gsl_sf_lambert_Wm1_e 1
# rf44 = lambda x: re(lambertw(x,-1)) if (x<0.0) & (x>(-1.0/2.71828182845904523536028747135)) else sf.lambert_W0(x)
rf44 = lambda x: re(lambertw(x,-1)) if (x<0.0) & (x>(-1.0/2.71828182845904523536028747135)) else sf.lambert_W0(x)


#gsl_sf_hydrogenicR_1_e 2
rf45 = lambda x,y: fmul(2.0*x,fmul(sqrt(x),exp(-fmul(x,y,exact=True)),exact=True),exact=True)


#gsl_sf_airy_Ai_deriv_e 1
rf46 = lambda x: airyai(x,1)


#gsl_sf_airy_Ai_deriv_scaled_e 1
rf47 = lambda x: fmul(exp(fmul(2.0/3.0,power(x,3.0/2.0),exact=True)),airyai(x,1),exact=True) if x>0 else airyai(x,1)


#gsl_sf_airy_Ai_e 1
rf48 = lambda x: airyai(x)


#gsl_sf_airy_Ai_scaled_e 1
rf49 = lambda x: fmul(exp(fmul(2.0/3.0,power(x,3.0/2.0),exact=True)),airyai(x),exact=True) if x>0 else airyai(x)


#gsl_sf_airy_Bi_deriv_e 1
rf50 = lambda x: airybi(x,1)


#gsl_sf_airy_Bi_deriv_scaled_e 1
rf51 = lambda x: fmul(exp(fmul(-2.0/3.0,power(x,3.0/2.0),exact=True)),airybi(x,1),exact=True) if x>0 else airybi(x,1)


#gsl_sf_airy_Bi_e 1
rf52 = lambda x: airybi(x)


#gsl_sf_airy_Bi_scaled_e 1
rf53 = lambda x: fmul(exp(fmul(-2.0/3.0,power(x,3.0/2.0),exact=True)),airybi(x),exact=True) if x>0 else airybi(x)


#gsl_sf_fermi_dirac_0_e 1
rf54 = lambda x: -1.0*polylog(1.0,-exp(x)) if x > -50.0 else exp(x)


#gsl_sf_fermi_dirac_1_e 1
rf55 = lambda x: -1.0*polylog(2.0,-exp(x)) if x > -50.0 else exp(x)


#gsl_sf_fermi_dirac_2_e 1
rf56 = lambda x: -1.0*polylog(3.0,-exp(x)) if x > -50.0 else exp(x)


#gsl_sf_fermi_dirac_3half_e 1
rf57 = lambda x: quad(lambda t: fmul(t,sqrt(t),exact=True)/(fadd(exp(fsub(t,x,exact=True)),1)),[0,inf])/gamma(2.5) if x > -50.0 else exp(x)


#gsl_sf_fermi_dirac_half_e 1
rf58 = lambda x: quad(lambda t: sqrt(t)/(fadd(exp(fsub(t,x,exact=True)),1)),[0,inf])/gamma(1.5) if x > -50.0 else exp(x)


#gsl_sf_fermi_dirac_inc_0_e 2
rf59 = lambda x,y: float(-1.0*polylog(1.0,-exp(y-x)))-(y-x) if y-x > -50.0 else float(exp(y-x))-(y-x)


#gsl_sf_fermi_dirac_m1_e 1
rf60 = lambda x: exp(x)/(fadd(1,exp(x),exact=True))


#gsl_sf_fermi_dirac_mhalf_e 1
rf61 = lambda x: quad(lambda t: 1/fmul(sqrt(t),(fadd(exp(fsub(t,x,exact=True)),1)),exact=True),[0,inf])/gamma(0.5) if x > -50.0 else exp(x)


#gsl_sf_conicalP_0_e 2
rf62 = lambda x,y: re(legenp(-0.5+j*x,0,y,type=3))

#gsl_sf_conicalP_1_e 2
rf63 = lambda x,y: re(legenp(-0.5+j*x,1,y,type=3))


#gsl_sf_conicalP_half_e 2
rf64 = lambda x,y: re(legenp(-0.5+j*x,0.5,y,type=3))


#gsl_sf_conicalP_mhalf_e 2
rf65 = lambda x,y: re(legenp(-0.5+j*x,-0.5,y,type=3))


#gsl_sf_legendre_H3d_0_e 2
rf66 = lambda x,y: sin(fmul(x,y,exact=True))/(fmul(x,sinh(y),exact=True))


#gsl_sf_legendre_H3d_1_e 2
rf67 = lambda x,y: fmul(sin(fmul(x,y)),(fsub(coth(y),x*cot(fmul(x,y)),exact=True)),exact=True)/fmul(sqrt(fadd(power(x,2.0),1.0,exact=True)),(fmul(x,sinh(y))),exact=True)


#gsl_sf_legendre_P1_e 1
rf68 = lambda x: legendre(1,x)


#gsl_sf_legendre_P2_e 1
rf69 = lambda x: legendre(2,x)


#gsl_sf_legendre_P3_e 1
rf70 = lambda x: legendre(3,x)


#gsl_sf_legendre_Q0_e 1
rf71 = lambda x: legenq(0,0,x,type=3).real


#gsl_sf_legendre_Q1_e 1
rf72 = lambda x: legenq(1,0,x,type=3).real


#gsl_sf_gegenpoly_1_e 2
rf73 = lambda x,y: gegenbauer(1,x,y,accurate_small=False)


#gsl_sf_gegenpoly_2_e 2
rf74 = lambda x,y: gegenbauer(2,x,y, accurate_small=False)


#gsl_sf_gegenpoly_3_e 2
rf75 = lambda x,y: gegenbauer(3,x,y, accurate_small=False) if x!=-2.0 else fmul(12,y,exact=True)


#gsl_sf_log_1plusx_e 1
rf76 = lambda x: log(fadd(1,x,exact=True))


#gsl_sf_log_1plusx_mx_e 1
rf77 = lambda x: fsub(log(fadd(1,x,exact=True)),x,exact=True)


#gsl_sf_log_abs_e 1
rf78 = lambda x: log(abs(x))


#gsl_sf_log_e 1
rf79 = lambda x: log(erfc(x))


#gsl_sf_cos_e 1
rf80 = lambda x: cos(x)


#gsl_sf_hypot_e 2
rf81 = lambda x,y: sqrt(fadd(power(x,2.0),power(y,2.0),exact=True))


#gsl_sf_lncosh_e 1
rf82 = lambda x: log(cosh(x))


#gsl_sf_lnsinh_e 1
rf83 = lambda x: log(sinh(x))


#gsl_sf_sin_e 1
rf84 = lambda x: sin(x)


#gsl_sf_sinc_e 1
rf85 = lambda x: sinc(fmul(np.pi,x,exact=True))


#gsl_sf_transport_2_e 1
rf86 = lambda x: quad(lambda t: fmul(power(t,2.0),exp(t),exact=True)/power((fsub(exp(t),1.0,exact=True)),2.0),[0,x])


#gsl_sf_transport_3_e 1
rf87 = lambda x: quad(lambda t: fmul(power(t,3.0),exp(t),exact=True)/power((fsub(exp(t),1.0)),2.0),[0,x])


#gsl_sf_transport_4_e 1
rf88 = lambda x: quad(lambda t: fmul(power(t,4.0),exp(t),exact=True)/power((fsub(exp(t),1.0)),2.0),[0,x])


#gsl_sf_transport_5_e 1
rf89 = lambda x: quad(lambda t: fmul(power(t,5.0),exp(t),exact=True)/power((fsub(exp(t),1.0)),2.0),[0,x])


#gsl_sf_synchrotron_1_e 1
rf90 = lambda x: fmul(x,quad(lambda t: besselk(5.0/3.0,t),[x,inf]),exact=True) if x< 60 else fmul(x,quad(lambda t: besselk(5.0/3.0,t),linspace(x,x+21,5)+[inf]),exact=True)


#gsl_sf_synchrotron_2_e 1
rf91 = lambda x: fmul(x,besselk(2.0/3.0,x),exact=True)


#gsl_sf_beta_e 2
rf92 = lambda x,y: beta(x,y)


#gsl_sf_beta_inc_e 3
rf93 = lambda x,y,z: re(betainc(x,y,0,z))/beta(x,y)


#gsl_sf_gamma_e 1
rf94 = lambda x: gamma(x)


#gsl_sf_gamma_inc_P_e 2
rf95 = lambda x,y: gammainc(x,0,y,regularized=True)


#gsl_sf_gamma_inc_Q_e 2
rf96 = lambda x,y: gammainc(x,y,regularized=True)


#gsl_sf_gamma_inc_e 2
rf97 = lambda x,y: gammainc(x,y)


#gsl_sf_gammainv_e 1
rf98 = lambda x: rgamma(x)


#gsl_sf_gammastar_e 1
rf99 = lambda x: gamma(x)/(fmul(sqrt(2*pi),fmul(power(x,(fsub(x,0.5,exact=True))),exp(-x),exact=True),exact=True))


#gsl_sf_lnbeta_e 2
rf100 = lambda x,y: ln(beta(x,y))


#gsl_sf_lngamma_e 1
rf101 = lambda x: loggamma(x)


#gsl_sf_lnpoch_e 2
rf102 = lambda x,y: fsub(loggamma(fadd(x,y,exact=True)),loggamma(x),exact=True)


#gsl_sf_poch_e 2
rf103 = lambda x,y: gamma(fadd(x,y,exact=True))/gamma(x)


#gsl_sf_pochrel_e 2
rf104 = lambda x,y: fsub(fdiv(gamma(fadd(x,y,exact=True)),gamma(x)),1,exact=True)/y


#gsl_sf_exp_e 1
rf105 = lambda x,y: fmul(y,exp(x),exact=True)


#gsl_sf_exp_mult_e 2
rf106 = lambda x,y: fmul(y,exp(x),exact=True)

#gsl_sf_expm1_e 1
rf107 = lambda x: expm1(x)


#gsl_sf_exprel_2_e 1
rf108 = lambda x: 2.0*(fsub(exp(x),fadd(1.0,x,exact=True),exact=True))/(power(x,2.0))


#gsl_sf_exprel_e 1
rf109 = lambda x: (fsub(exp(x),1,exact=True))/x


#gsl_sf_debye_1_e 1
rf110 = lambda x: quad(lambda t: power(t,1)/(exp(t)-1),[0,x])/x


#gsl_sf_debye_2_e 1
rf111 = lambda x: 2.0 * quad(lambda t: power(t,2.0)/(exp(t)-1),[0,x])/power(x,2.0)


#gsl_sf_debye_3_e 1
rf112 = lambda x: 3.0 * quad(lambda t: power(t,3.0)/(exp(t)-1),[0,x])/power(x,3.0)


#gsl_sf_debye_4_e 1
rf113 = lambda x: 4.0 * quad(lambda t: power(t,4.0)/(exp(t)-1),[0,x])/power(x,4.0)


#gsl_sf_debye_5_e 1
rf114 = lambda x: 5.0 * quad(lambda t: power(t,5.0)/(exp(t)-1),[0,x])/power(x,5.0)


#gsl_sf_debye_6_e 1
rf115 = lambda x: 6.0 * quad(lambda t: power(t,6.0)/(exp(t)-1.0),[0,x])/power(x,6.0)


#gsl_sf_psi_1_e 1
rf116 = lambda x: re(psi(0,1+x*j))


#gsl_sf_psi_1piy_e 1
rf117 = lambda x: re(psi(0,1+x*j))


#gsl_sf_psi_e 1
rf118 = lambda x: digamma(x)


#gsl_sf_hyperg_0F1_e 2
rf119 = lambda x,y: hyp0f1(x,y)


#gsl_sf_hyperg_1F1_e 3
rf120 = lambda x,y,z: hyp1f1(x,y,z)


#gsl_sf_hyperg_2F0_e 3
rf121 = lambda x,y,z: hyp2f0(x,y,z)


#gsl_sf_hyperg_2F1_conj_e 4
rf122 = lambda x,y,z,p: re(hyp2f1(x+y*j,x-y*j,z,p))


#gsl_sf_hyperg_2F1_conj_renorm_e 4
rf123 = lambda x,y,z,p: re(hyp2f1(x+y*j,x-y*j,z,p))/gamma(z)


#gsl_sf_hyperg_2F1_e 4
rf124 = lambda x,y,z,p: hyp2f1(x,y,z,p)


#gsl_sf_hyperg_2F1_renorm_e 4
rf125 = lambda x,y,z,p: hyp2f1(x,y,z,p)/gamma(z)


#gsl_sf_hyperg_U_e 3
rf126 = lambda x,y,z: power(z,-x)*hyp2f0(x,1.0+x-y,power(-z,-1.0))


#gsl_sf_dawson_e 1
rf127 = lambda x: fmul(sqrt(pi),fmul(exp(-x*x),erfi(x),exact=True),exact=True)/2.0


#gsl_sf_ellint_D_e 2
rf128 = lambda x,y: pow(np.sin(x),3.0)/3.0 * elliprd(1-pow(np.sin(x),2.0),1-pow(y,2.0)*pow(np.sin(x),2.0),1.0) if floor(x/np.pi + 0.5) == 0 else 2.0*floor(x/np.pi + 0.5)*elliprd(0.0,1-y*y,1.0)/3.0

#gsl_sf_ellint_Dcomp_e 1
rf129 = lambda y: 2.0*elliprd(0.0,1-y*y,1.0)/3.0

#gsl_sf_ellint_E_e 2
rf130 = lambda x,y: ellipe(x,y*y)


#gsl_sf_ellint_Ecomp_e 1
rf131 = lambda x: ellipe(power(x,2.0))


#gsl_sf_ellint_F_e 2
rf132 = lambda x,y: ellipf(x,y*y)


#gsl_sf_ellint_Kcomp_e 1
rf133 = lambda x: ellipk(power(x,2.0))


#gsl_sf_ellint_P_e 3
rf134 = lambda x,y,z: ellippi(-z,x,y*y)


#gsl_sf_ellint_Pcomp_e 2
rf135 = lambda x,y: fsub(elliprf(0.0,fsub(1.0,power(x,2.0),exact=True),1.0),fmul((y),elliprj(0.0,fsub(1.0,power(x,2.0),exact=True),1.0,fadd(1.0,y,exact=True)),exact=True)/3.0,exact=True)


#gsl_sf_ellint_RC_e 2
rf136 = lambda x,y: elliprc(x,y)


#gsl_sf_ellint_RD_e 3
rf137 = lambda x,y,z: elliprd(x,y,z)


#gsl_sf_ellint_RF_e 3
rf138 = lambda x,y,z: elliprf(x,y,z)


#gsl_sf_ellint_RJ_e 4
rf139 = lambda x,y,z,p: elliprj(x,y,z,p)


#gsl_sf_eta_e 1
rf140 = lambda x: altzeta(x)


#gsl_sf_hzeta_e 2
rf141 = lambda x,y: autoprec(zeta)(x,y)


#gsl_sf_zeta_e 1
rf142 = lambda x: zeta(x)


#gsl_sf_zetam1_e 1
rf143 = lambda x: fsub(zeta(x),1)


#gsl_sf_cos_pi_e 1
rf144 = 0.0

#gsl_sf_sin_pi_e 1
rf145 = 0.0

#gsl_sf_Chi_e 1
rf146 = lambda x: chi(x)


#gsl_sf_Ci_e 1
rf147 = lambda x: ci(x)


#gsl_sf_Shi_e 1
rf148 = lambda x: shi(x)


#gsl_sf_Si_e 1
rf149 = lambda x: si(x)


#gsl_sf_atanint_e 1
rf150 = lambda x: quad(lambda t: atan(t)/t,[0,x])


#gsl_sf_expint_3_e 1
rf151 = lambda x: quad(lambda t: exp(-power(t,3.0)),[0,x])


#gsl_sf_expint_E1_e 1
rf152 = lambda x: expint(1,x)


#gsl_sf_expint_E1_scaled_e 1
rf153 = 0.0

#gsl_sf_expint_E2_e 1
rf154 = lambda x: expint(2,x)


#gsl_sf_expint_E2_scaled_e 1
rf155 = 0.0

#gsl_sf_expint_Ei_e 1
rf156 = lambda x: ei(x)

#gsl_sf_expint_Ei_scaled_e 1
rf157 = 0.0

rfl = [rf0,rf1,rf2,rf3,rf4,rf5,rf6,rf7,rf8,rf9,rf10,rf11,rf12,rf13,rf14,rf15,rf16,rf17,rf18,rf19,rf20,rf21,rf22,rf23,rf24,rf25,rf26,rf27,rf28,rf29,rf30,rf31,rf32,rf33,rf34,rf35,rf36,rf37,rf38,rf39,rf40,rf41,rf42,rf43,rf44,rf45,rf46,rf47,rf48,rf49,rf50,rf51,rf52,rf53,rf54,rf55,rf56,rf57,rf58,rf59,rf60,rf61,rf62,rf63,rf64,rf65,rf66,rf67,rf68,rf69,rf70,rf71,rf72,rf73,rf74,rf75,rf76,rf77,rf78,rf79,rf80,rf81,rf82,rf83,rf84,rf85,rf86,rf87,rf88,rf89,rf90,rf91,rf92,rf93,rf94,rf95,rf96,rf97,rf98,rf99,rf100,rf101,rf102,rf103,rf104,rf105,rf106,rf107,rf108,rf109,rf110,rf111,rf112,rf113,rf114,rf115,rf116,rf117,rf118,rf119,rf120,rf121,rf122,rf123,rf124,rf125,rf126,rf127,rf128,rf129,rf130,rf131,rf132,rf133,rf134,rf135,rf136,rf137,rf138,rf139,rf140,rf141,rf142,rf143,rf144,rf145,rf146,rf147,rf148,rf149,rf150,rf151,rf152,rf153,rf154,rf155,rf156,rf157]
