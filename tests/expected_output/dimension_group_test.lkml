view: dimension_group_test {

  dimension_group: dimension1 {
    type: time
    timeframes: [time, date, week, month]
    datatype: datetime
    sql: ${TABLE}.dim1 ;;
  }
}
