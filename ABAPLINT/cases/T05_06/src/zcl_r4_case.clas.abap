class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    data row type zr4_data.
    row-id = 9.
    row-amount = 10.
    insert zr4_data from @row.
    if sy-subrc <> 0.
      rv = -999.
      return.
    endif.
    commit work.
    select sum( amount ) from zr4_data into @rv.
  endmethod.
endclass.
