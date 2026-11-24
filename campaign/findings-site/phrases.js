// Data-driven Spanish phrasing shared by index.html and report.html. Any sentence whose
// wording depends on the data (multipliers, "uno de cada N", whether an interval clears
// zero, whether a difference is significant) is built here from window.SG_DATA, so it
// follows the dump instead of being hardcoded. Single source for these claims.
var SG_PH = (function () {
  var W = { 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez" };
  function word(n) { return W[n] || String(n); }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  // 26 -> "uno de cada cuatro"
  function oneIn(pct, fem) { return (fem ? "una" : "uno") + " de cada " + word(Math.round(100 / pct)); }
  // 3.2 -> "más de tres veces", 4.1 -> "unas cuatro veces"
  function times(m) { var f = Math.floor(m); return (m - f >= 0.15) ? "más de " + word(f) + " veces" : "unas " + word(Math.round(m)) + " veces"; }

  // Adjusted gender residual (analytic HC3 robust CI). Wording switches on whether the CI clears zero.
  function residual(R) {
    var ci = R.adjusted_ci_hc3, lo = Math.round(ci[0]), hi = Math.round(ci[1]), pt = Math.round(R.adjusted_point);
    var clears = ci[0] > 0;
    var bounds = "El efecto del género queda acotado entre ~" + R.bounds_lower + "% emparejando todo y " + R.bounds_upper + "% sin ajustar.";
    return {
      cap: "Brecha ajustada, por conjunto de controles. Con todo ajustado queda ~" + pt + "% (IC 95% " + lo + "% a " + hi + "%, p=" + R.adjusted_p + "). Estable entre tipos de cambio 17 y 20.",
      line: (clears
        ? "Ese ~" + pt + "% ya se distingue del cero, aunque por poco. Es una multa real, pero chica e imprecisa, así que no la convertimos en pesos. "
        : "Ese ~" + pt + "% tiene un intervalo de confianza que toca el cero, así que no afirmamos un castigo fijo por el mismo trabajo. ")
        + bounds + " La brecha es, sobre todo, de progresión.",
      method: "La brecha de género es el único punto con un modelo de controles. " + bounds + " "
        + (clears
          ? "El residuo totalmente ajustado, de ~" + pt + "%, apenas se distingue del cero (IC 95% " + lo + "% a " + hi + "%). Es chico e impreciso, por eso no se convierte a pesos."
          : "El residuo totalmente ajustado, de ~" + pt + "%, tiene un intervalo que toca el cero.")
        + " Controlar por nivel y rol, que en parte son consecuencia del mismo sesgo, probablemente subestima el efecto."
        + " No lo llamamos discriminación probada. También contiene factores que la encuesta no mide."
    };
  }

  // Agentic-coding adoption by gender among developers. Wording switches on Fisher's exact p.
  function aiGender(A) {
    var base = "Entre quienes desarrollan software, " + A.men_pct + "% de los hombres ya instruye a los agentes, contra " + A.women_pct + "% de las mujeres. ";
    return A.fisher_p < 0.05
      ? base + "La diferencia es estadísticamente significativa."
      : base + "Es una señal que vigilar, no una conclusión. Con solo " + A.women_n + " mujeres desarrolladoras en la muestra, la diferencia todavía no es estadísticamente concluyente.";
  }

  // AI-focused roles: compare women's share of the roles to their share of respondents
  // (a raw head count would mostly reflect that the sample has more men).
  function aiRoles(roles, participation) {
    var w = Math.round(100 * roles.women / (roles.men + roles.women));
    return "Las mujeres ocupan " + w + "% de estos puestos (" + roles.women + " contra " + roles.men + " hombres), por debajo de su " + participation + "% de participación en la encuesta.";
  }

  return { word: word, cap: cap, oneIn: oneIn, times: times, residual: residual, aiGender: aiGender, aiRoles: aiRoles };
})();
