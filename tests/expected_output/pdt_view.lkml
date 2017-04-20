view: pdt_view {

  derived_table: {
    sql: SELECT id, count(*) c FROM table GROUP BY id ;;
    sql_trigger_value: DATE() ;;
    indexes: ["id"]
  }

  dimension: c {
    type: number
    sql: ${TABLE}.c ;;
  }

  dimension: id {
    type: number
    primary_key: yes
    sql: ${TABLE}.id ;;
  }

  measure: sum_c {
    type: sum
    sql: ${TABLE}.c ;;
  }
}
