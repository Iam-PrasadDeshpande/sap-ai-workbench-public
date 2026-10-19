class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    read entities of zr4_missing
      entity Item
      all fields with value #( ( id = 1 ) )
      result data(items).
    rv = lines( items ).
  endmethod.
endclass.
