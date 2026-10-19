class zcl_r4_case definition public final create public.
  public section.
    methods run returning value(rv) type i.

endclass.
class zcl_r4_case implementation.
  method run.
    types: begin of row_type,
      id type i,
      amount type i,
    end of row_type.
    data rows type standard table of row_type with empty key.
    rows = value #( ( id = 1 amount = 5 ) ( id = 2 amount = 7 ) ).
    select sum( amount ) from @rows as row into @rv.
  endmethod.
endclass.
