class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    authority-check object 'S_TCODE' id 'TCD' field 'SE38'.
    rv = 1.
  endmethod.
endclass.
