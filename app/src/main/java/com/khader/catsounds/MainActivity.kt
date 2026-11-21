package com.khader.catsounds

import android.app.Activity
import android.app.AlertDialog
import android.content.Intent
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.media.MediaPlayer
import android.net.Uri
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.GridLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.SeekBar
import android.widget.TextView
import android.widget.Toast

class MainActivity : Activity() {
    private lateinit var prefs: SharedPreferences
    private var player: MediaPlayer? = null
    private var playingId = -1
    private var pendingId = -1
    private var volume = 1f
    private val tiles = HashMap<Int, TextView>()
    private val colors = intArrayOf(
        0xFFC2185B.toInt(), 0xFFEF6C00.toInt(), 0xFF1976D2.toInt(), 0xFFC62828.toInt(), 0xFF6A1B9A.toInt(),
        0xFF2E7D32.toInt(), 0xFF00838F.toInt(), 0xFF5D4037.toInt(), 0xFF303F9F.toInt(), 0xFFAD1457.toInt()
    )

    private fun dp(v: Int) = (v * resources.displayMetrics.density).toInt()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        prefs = getSharedPreferences("cats", MODE_PRIVATE)
        volume = prefs.getFloat("volume", 1f)
        val bg = Color.parseColor("#14110F")
        window.statusBarColor = bg
        window.navigationBarColor = bg

        val root = LinearLayout(this)
        root.orientation = LinearLayout.VERTICAL
        root.setBackgroundColor(bg)
        root.layoutDirection = View.LAYOUT_DIRECTION_RTL

        val header = LinearLayout(this)
        header.orientation = LinearLayout.HORIZONTAL
        header.gravity = Gravity.CENTER_VERTICAL
        header.setPadding(dp(16), dp(14), dp(16), dp(8))
        val title = TextView(this)
        title.text = "🐱 أصوات القطط"
        title.textSize = 22f
        title.setTextColor(Color.parseColor("#FF8A1F"))
        title.typeface = Typeface.DEFAULT_BOLD
        header.addView(title, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        val gear = TextView(this)
        gear.text = "⚙️"
        gear.textSize = 24f
        gear.setPadding(dp(10), dp(4), dp(10), dp(4))
        gear.setOnClickListener { settingsDialog() }
        header.addView(gear)
        root.addView(header)

        val hint = TextView(this)
        hint.text = "اضغط للتشغيل • اضغط مطوّلاً لتغيير الصوت من جوالك"
        hint.textSize = 12f
        hint.setTextColor(Color.parseColor("#9E9488"))
        hint.setPadding(dp(16), 0, dp(16), dp(6))
        root.addView(hint)

        val content = LinearLayout(this)
        content.orientation = LinearLayout.VERTICAL
        content.setPadding(dp(8), 0, dp(8), dp(24))
        for ((ci, cname) in CATEGORIES.withIndex()) {
            val h = TextView(this)
            h.text = cname
            h.textSize = 16f
            h.typeface = Typeface.DEFAULT_BOLD
            h.setTextColor(Color.WHITE)
            h.setPadding(dp(8), dp(16), dp(8), dp(4))
            content.addView(h)
            val grid = GridLayout(this)
            grid.columnCount = 3
            for (c in CATS.filter { it.cat == ci }) {
                val t = TextView(this)
                t.gravity = Gravity.CENTER
                t.textSize = 13f
                t.maxLines = 3
                t.setTextColor(Color.WHITE)
                t.setPadding(dp(4), dp(6), dp(4), dp(6))
                val lp = GridLayout.LayoutParams(GridLayout.spec(GridLayout.UNDEFINED), GridLayout.spec(GridLayout.UNDEFINED, 1f))
                lp.width = 0
                lp.height = dp(92)
                lp.setMargins(dp(4), dp(4), dp(4), dp(4))
                t.layoutParams = lp
                t.setOnClickListener { play(c.id) }
                t.setOnLongClickListener { soundDialog(c.id); true }
                tiles[c.id] = t
                refresh(c)
                grid.addView(t)
            }
            content.addView(grid)
        }
        val scroll = ScrollView(this)
        scroll.addView(content)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))
        setContentView(root)
    }

    private fun refresh(c: Cat, active: Boolean = false) {
        val t = tiles[c.id] ?: return
        val mark = if (prefs.contains("custom_${c.id}")) " ✦" else ""
        t.text = "${c.emoji}\n${c.name}$mark"
        t.textSize = 13f
        val d = GradientDrawable()
        d.cornerRadius = dp(16).toFloat()
        d.setColor(colors[c.cat % colors.size])
        if (active) d.setStroke(dp(3), Color.WHITE)
        t.background = d
        t.alpha = if (active) 1f else 0.92f
    }

    private fun play(id: Int) {
        stopPlayer()
        val uriStr = prefs.getString("custom_$id", null)
        var mp: MediaPlayer? = null
        if (uriStr != null) {
            mp = try {
                MediaPlayer().also { it.setDataSource(this, Uri.parse(uriStr)); it.prepare() }
            } catch (e: Exception) {
                Toast.makeText(this, "تعذّر تشغيل الصوت المخصص، سيُستخدم الأصلي", Toast.LENGTH_SHORT).show()
                null
            }
        }
        if (mp == null) {
            val rid = resources.getIdentifier(String.format("cat_%03d", id), "raw", packageName)
            mp = MediaPlayer.create(this, rid)
        }
        val m = mp ?: return
        m.setVolume(volume, volume)
        m.setOnCompletionListener { stopPlayer() }
        player = m
        playingId = id
        refresh(CATS[id - 1], true)
        tiles[id]?.animate()?.scaleX(0.93f)?.scaleY(0.93f)?.setDuration(80)?.withEndAction {
            tiles[id]?.animate()?.scaleX(1f)?.scaleY(1f)?.setDuration(120)?.start()
        }?.start()
        m.start()
    }

    private fun stopPlayer() {
        player?.let {
            try { if (it.isPlaying) it.stop() } catch (e: Exception) { }
            it.release()
        }
        player = null
        if (playingId > 0) refresh(CATS[playingId - 1])
        playingId = -1
    }

    private fun soundDialog(id: Int) {
        val c = CATS[id - 1]
        val items = if (prefs.contains("custom_$id"))
            arrayOf("🎵 اختيار صوت من الجوال", "↩️ استعادة الصوت الأصلي")
        else arrayOf("🎵 اختيار صوت من الجوال")
        AlertDialog.Builder(this).setTitle("${c.emoji} ${c.name}")
            .setItems(items) { _, w -> if (w == 0) pick(id) else resetOne(id) }.show()
    }

    private fun pick(id: Int) {
        pendingId = id
        val i = Intent(Intent.ACTION_OPEN_DOCUMENT)
        i.addCategory(Intent.CATEGORY_OPENABLE)
        i.type = "audio/*"
        i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
        startActivityForResult(i, 77)
    }

    private fun resetOne(id: Int) {
        prefs.edit().remove("custom_$id").apply()
        refresh(CATS[id - 1])
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != 77 || resultCode != RESULT_OK || pendingId < 1) return
        val uri = data?.data ?: return
        try {
            contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
        } catch (e: Exception) { }
        prefs.edit().putString("custom_$pendingId", uri.toString()).apply()
        val id = pendingId
        pendingId = -1
        refresh(CATS[id - 1])
        Toast.makeText(this, "تم حفظ الصوت ✦", Toast.LENGTH_SHORT).show()
        play(id)
    }

    private fun settingsDialog() {
        val box = LinearLayout(this)
        box.orientation = LinearLayout.VERTICAL
        box.layoutDirection = View.LAYOUT_DIRECTION_RTL
        box.setPadding(dp(20), dp(12), dp(20), dp(4))
        val vl = TextView(this)
        vl.text = "🔊 مستوى الصوت"
        box.addView(vl)
        val sb = SeekBar(this)
        sb.max = 100
        sb.progress = (volume * 100).toInt()
        sb.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(s: SeekBar?, p: Int, u: Boolean) {
                volume = p / 100f
                prefs.edit().putFloat("volume", volume).apply()
                player?.setVolume(volume, volume)
            }
            override fun onStartTrackingTouch(s: SeekBar?) {}
            override fun onStopTrackingTouch(s: SeekBar?) {}
        })
        box.addView(sb)
        fun btn(text: String, action: () -> Unit) {
            val b = TextView(this)
            b.text = text
            b.textSize = 16f
            b.setPadding(0, dp(14), 0, dp(14))
            b.setOnClickListener { action() }
            box.addView(b)
        }
        val dlg = AlertDialog.Builder(this).setTitle("⚙️ الإعدادات").setView(box)
            .setPositiveButton("تم", null).create()
        btn("🎵 إضافة صوت من الجوال لزر") { dlg.dismiss(); chooseButton() }
        btn("↩️ استعادة كل الأصوات الأصلية") {
            dlg.dismiss()
            AlertDialog.Builder(this).setMessage("حذف كل الأصوات المخصصة؟")
                .setPositiveButton("نعم") { _, _ ->
                    val e = prefs.edit()
                    for (c in CATS) e.remove("custom_${c.id}")
                    e.apply()
                    for (c in CATS) refresh(c)
                }.setNegativeButton("لا", null).show()
        }
        val about = TextView(this)
        about.text = "المطوّر: khader abo salha"
        about.textSize = 12f
        about.setTextColor(Color.parseColor("#9E9488"))
        about.setPadding(0, dp(10), 0, dp(6))
        box.addView(about)
        dlg.show()
    }

    private fun chooseButton() {
        val names = Array(CATS.size) { "${CATS[it].emoji} ${CATS[it].name}" }
        AlertDialog.Builder(this).setTitle("اختر الزر")
            .setItems(names) { _, w -> pick(CATS[w].id) }.show()
    }

    override fun onDestroy() {
        stopPlayer()
        super.onDestroy()
    }
}
