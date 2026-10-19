class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    data ref type ref to zif_r4_missing.
    if ref is bound.
      rv = 1.
    endif.
  endmethod.
endclass.
