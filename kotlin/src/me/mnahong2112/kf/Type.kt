package me.mnahong2112.kf

import kotlin.coroutines.experimental.EmptyCoroutineContext.plus

/**
 * Created by manhong2112 on 9/9/2017.
 */

sealed class KfObject {
   class KfNumber {

   }
   class KfString(val str: String) {

   }
   class KfFunction {

   }
   class KfChar {

   }
}

