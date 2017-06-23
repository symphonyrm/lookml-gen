view: newlines_test {

  dimension: a {
    type: number
    sql: ${TABLE}.a ;;
  }

  dimension: b {
    type: number
    sql: ${TABLE}.b ;;
  }

  dimension: c {
    type: number
    sql: ${TABLE}.c ;;
  }

  dimension: d {
    type: number
    sql: ${TABLE}.d ;;
  }

  measure: sum_a {
    type: sum
    sql: ${a} ;;
  }

  measure: sum_b {
    type: sum
    sql: ${b} ;;
  }

  measure: sum_c {
    type: sum
    sql: ${c} ;;
  }

  measure: sum_d {
    type: sum
    sql: ${d} ;;
  }
}
