class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    select sum( amount ) from zr4_data client specified into rv.
    if sy-subrc <> 0.
      rv = -999.
    endif.
  endmethod.
endclass.
