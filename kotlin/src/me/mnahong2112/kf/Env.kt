package me.mnahong2112.kf

/**
 * Created by manhong2112 on 9/9/2017.
 */
class Env {
   val env : HashMap<Pair<Scope, Symbol>, KfObject> = HashMap()

}

open class Scope(val id: Int, val previous: Scope?) {
   object RootScope : Scope(0, null)

   companion object {
      private var id = 0
      val rootScope: Scope = RootScope
   }

   fun next(id : Int = -1): Scope {
      if (id == -1) {
         Scope.id += 1
         return Scope(Scope.id, this)
      }
      return Scope(id, this)
   }

   fun back(id : Int = -1): Scope? {
      return previous
   }

}

open class Symbol(val value: String) {
   val hash by lazy {
      value.hashCode()
   }
   override fun hashCode(): Int {
      return hash
   }

   override fun equals(other: Any?): Boolean {
      if (this === other) return true
      if (other?.javaClass != javaClass) return false

      other as Symbol

      if (value != other.value) return false

      return true
   }
}