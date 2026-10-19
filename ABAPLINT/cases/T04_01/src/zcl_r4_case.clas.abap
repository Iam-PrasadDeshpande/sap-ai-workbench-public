class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    authority-check object 'S_TCODE' id 'TCD' field 'SE38'.
    if sy-subrc = 0.
      rv = 1.
    else.
      rv = 0.
    endif.
  endmethod.
endclass.
