#pragma OPENCL EXTENSION cl_khr_fp64 : enable  
#pragma OPENCL EXTENSION cl_khr_fp16 : enable  
#pragma OPENCL EXTENSION cl_khr_int64_base_atomics : enable  
__kernel void matmulUnroll4WithResidual(__global long *_kernel_context, __constant uchar *_constant_region, __local uchar *_local_region, __global int *_atomics, __global uchar *xout, __global uchar *x, __global uchar *w, __private int n, __private int d, __global uchar *positionAndLayer)
{
  float f_38, f_54, f_21, f_53, f_33, f_64, f_63, f_28, f_43, f_57, f_56, f_55; 
  int i_58, i_59, i_65, i_5, i_6, i_7, i_8, i_9, i_10, i_11, i_13, i_14, i_15, i_16, i_17, i_18, i_19, i_20, i_22, i_23, i_24, i_29, i_34, i_39, i_46, i_47; 
  float4 v4f_52; 
  long l_26, l_60, l_61, l_30, l_31, l_50, l_25, l_48, l_49, l_35, l_36, l_40, l_41; 
  ulong ul_3, ul_2, ul_1, ul_0, ul_32, ul_62, ul_42, ul_37, ul_4, ul_51, ul_45, ul_12, ul_44, ul_27; 

  // BLOCK 0
  ul_0  =  (ulong) xout;
  ul_1  =  (ulong) x;
  ul_2  =  (ulong) w;
  ul_3  =  (ulong) positionAndLayer;
  ul_4  =  ul_3 + 28L;
  i_5  =  *((__global int *) ul_4);
  i_6  =  i_5 << 24;
  i_7  =  i_6 >> 31;
  i_8  =  i_7 >> 30;
  i_9  =  i_8 + i_6;
  i_10  =  i_9 >> 2;
  i_11  =  get_global_size(0);
  ul_12  =  ul_2 + 24L;
  i_13  =  get_global_id(0);
  // BLOCK 1 MERGES [0 5 ]
  i_14  =  i_13;
  for(;i_14 < 2048;)
  {
    // BLOCK 2
    i_15  =  i_14 << 13;
    i_16  =  i_15 >> 31;
    i_17  =  i_16 >> 30;
    i_18  =  i_17 + i_15;
    i_19  =  i_18 >> 2;
    i_20  =  i_10 + i_19;
    // BLOCK 3 MERGES [2 4 ]
    f_21  =  0.0F;
    i_22  =  0;
    for(;i_22 < 2048;)
    {
      // BLOCK 4
      i_23  =  i_22 << 2;
      i_24  =  i_23 + 6;
      l_25  =  (long) i_24;
      l_26  =  l_25 << 2;
      ul_27  =  ul_1 + l_26;
      f_28  =  *((__global float *) ul_27);
      i_29  =  i_23 + 7;
      l_30  =  (long) i_29;
      l_31  =  l_30 << 2;
      ul_32  =  ul_1 + l_31;
      f_33  =  *((__global float *) ul_32);
      i_34  =  i_23 + 8;
      l_35  =  (long) i_34;
      l_36  =  l_35 << 2;
      ul_37  =  ul_1 + l_36;
      f_38  =  *((__global float *) ul_37);
      i_39  =  i_23 + 9;
      l_40  =  (long) i_39;
      l_41  =  l_40 << 2;
      ul_42  =  ul_1 + l_41;
      f_43  =  *((__global float *) ul_42);
      ul_44  =  *((__global ulong *) ul_12);
      ul_45  =  ul_2 + ul_44;
      i_46  =  i_20 + i_22;
      i_47  =  i_46 << 2;
      l_48  =  (long) i_47;
      l_49  =  l_48 << 2;
      l_50  =  l_49 + 24L;
      ul_51  =  ul_45 + l_50;
      v4f_52  =  vload4(0, (__global float *) ul_51);
      f_53  =  v4f_52.s1 * f_33;
      f_54  =  fma(v4f_52.s0, f_28, f_53);
      f_55  =  fma(v4f_52.s2, f_38, f_54);
      f_56  =  fma(v4f_52.s3, f_43, f_55);
      f_57  =  f_21 + f_56;
      i_58  =  i_22 + 1;
      f_21  =  f_57;
      i_22  =  i_58;
    }  // B4
    // BLOCK 5
    i_59  =  i_14 + 6;
    l_60  =  (long) i_59;
    l_61  =  l_60 << 2;
    ul_62  =  ul_0 + l_61;
    f_63  =  *((__global float *) ul_62);
    f_64  =  f_63 + f_21;
    *((__global float *) ul_62)  =  f_64;
    i_65  =  i_11 + i_14;
    i_14  =  i_65;
  }  // B5
  // BLOCK 6
  return;
}  //  kernel

