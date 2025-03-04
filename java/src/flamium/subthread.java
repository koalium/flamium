/*
 * The MIT License
 *
 * Copyright 2024 koalium.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
package flamium;

import com.fazecast.jSerialComm.SerialPort;
import static flamium.main.sp;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 *
 * @author koalium
 */
public class subthread extends Thread{
	
	/**
	 *
	 */
	public subthread(){
		//subflame.
	}
	
	//
	public void fireIntheHole() {
		byte[] bufferb = {'f', 'i', 'r', 'e', '8', 0, '\n'};
		int bufferbindexreader = 0;
		int[] serbuffbyte = new int[500000];
		long st = System.currentTimeMillis();
		Boolean checkpoint_0 = false;
		Boolean checkpoint_1 = false;
		sp.setComPortTimeouts(SerialPort.TIMEOUT_NONBLOCKING, 2000, 2000);
		// Writing to binary file
		sp.writeBytes(bufferb, bufferb.length);
		try {
			OutputStream Stream;
			OutputStream datastream;
			OutputStream datastringstream;
			OutputStream timestream;
			try (InputStream inputStream = sp.getInputStream()) {
				Stream = new FileOutputStream("log.bin");
				datastream = new FileOutputStream("log_pressure.bin");
				datastringstream = new FileOutputStream("log_pressure.txt");
				timestream = new FileOutputStream("log_ir.txt");
				while (System.currentTimeMillis() - st < 8800) {
					if (sp.bytesAvailable() > 0) {
						serbuffbyte[bufferbindexreader++] = inputStream.read();

					}

				}
				int i = 0;
				while (i < bufferbindexreader) {
					Stream.write(serbuffbyte[i]);
					if (i++ < 5) {
						continue;
					}
					if (checkpoint_0 == false) {
						if ((serbuffbyte[i] == 0) && (serbuffbyte[i - 1] == 127) && (serbuffbyte[i - 2] == 0) && (serbuffbyte[i - 3] == 127) && (serbuffbyte[i - 4] == 0)) {
							checkpoint_0 = true;

						}
					} else if (checkpoint_1 == false) {

						if ((serbuffbyte[i] == 0) && (serbuffbyte[i + 1] == 127) && (serbuffbyte[i + 2] == 0) && (serbuffbyte[i + 3] == 127) && (serbuffbyte[i + 4] == 0)) {
							checkpoint_1 = true;
						}
					} else {

					}
					if (checkpoint_0 && !checkpoint_1) {
						datastream.write(serbuffbyte[i + 1]);
						datastringstream.write(byteParser(serbuffbyte[i + 1]));
					}
					if (checkpoint_1) {
						timestream.write(serbuffbyte[i + 5]);
					}

				}

			}
			datastringstream.close();
			timestream.close();
			Stream.close();
			datastream.close();
			sp.closePort();
			// Stream.write(new byte[]{0x48, 0x65, 0x6C, 0x6C, 0x6F}); 

			// ASCII values for "Hello"
			// Reading from a binary file
		} catch (IOException e) {
		}
	}
	//open the input and output streams
	//pre style="font-size: 11px;": an open port
	//post: initialized input and output streams for use to communicate data

	public boolean serialSend(String ss) {
		//return value for whether opening the streams is successful or not
		if (sp.isOpen()) {
			sp.writeBytes(ss.getBytes(), ss.getBytes().length);
			return true;
		}

		return false;
	}

	public int readpiezovalue() throws FileNotFoundException, IOException {
		if (!sp.isOpen()) {

			sp.openPort(2500);
			if (!sp.isOpen()) {
				return 0;
			}
		}

		serialSend(_str_piezotest_);
		int[] ii = terminalReadAscci(sp);
		int c = 0;
		for(c=0;c<ii.length;c++){
			if(ii[c]=='\n'){
				break;
			}
		}
		int calvalue = ii[c]+ii[c+1];
		//jLabelShowTerminal.setText(gstr.substring(0, 4) + " " + calvalue);
		OutputStream Stream = new FileOutputStream("calibre.bin");
		Stream.write(calvalue);
		
		return calvalue;
	}

	public int[] terminalReadAscci(SerialPort sp_) {
		int[] ii = new int[255];
		if (!sp_.isOpen()) {
			return ii;
		}
		char inchar;

		int iicounter = 0;

		sp_.setComPortTimeouts(SerialPort.TIMEOUT_READ_SEMI_BLOCKING, 1000, 1000);
		long st = System.currentTimeMillis();
		try (InputStream inputStream = sp.getInputStream()) {
			while (sp.bytesAvailable() > 0) {//&&System.currentTimeMillis()<st+1000 ){
				inchar = (char) inputStream.read();
				ii[iicounter++] = (int) (inchar);
				gstr += inchar;
			}

		} catch (IOException e) {
		}
		return ii;
	}

	//
	public void writeToFile(int[] data, int size, String filename) throws FileNotFoundException {
		OutputStream Stream;
		Stream = new FileOutputStream(filename);
		int i = 0;
		while (i < size) {
			try {
				Stream.write(data[i]);
				Stream.close();
			} catch (IOException ex) {
				Logger.getLogger(main.class.getName()).log(Level.SEVERE, null, ex);
			}
		}

	}

	byte[] byteParser(int b) {
		String s = String.valueOf(b);
		return (s + "\n").getBytes();
	}

	//
	/**
	 * @param args the command line arguments
	 */
	public static void main(String args[]) {
		/* Set the Nimbus look and feel */
		//<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
		/* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
		 */
		try {
			for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
				if ("Nimbus".equals(info.getName())) {
					javax.swing.UIManager.setLookAndFeel(info.getClassName());
					break;
				}
			}
		} catch (ClassNotFoundException ex) {
			java.util.logging.Logger.getLogger(main.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		} catch (InstantiationException ex) {
			java.util.logging.Logger.getLogger(main.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		} catch (IllegalAccessException ex) {
			java.util.logging.Logger.getLogger(main.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		} catch (javax.swing.UnsupportedLookAndFeelException ex) {
			java.util.logging.Logger.getLogger(main.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		}
		//</editor-fold>
		//</editor-fold>

		/* Create and display the form */
		java.awt.EventQueue.invokeLater(() -> {
			try {
				new main().setVisible(true);
			} catch (IOException | InterruptedException ex) {
				Logger.getLogger(main.class.getName()).log(Level.SEVERE, null, ex);
			}
		});
		
		/* Create and display the form */
		java.awt.EventQueue.invokeLater(() -> {
			
			flmgrp = new FlamiumGraph();
			flmgrp.setVisible(true);
		});
		
		java.awt.EventQueue.invokeLater(() -> {
			
			flmg = new FlamiumGui();
			flmg.setVisible(true);
		});
		
		/* Create and display the form */
		java.awt.EventQueue.invokeLater(() -> {
			
			flmmq = new FlamiumMq();
			flmmq.setVisible(true);
		});
		
		/* Create and display the form */
		java.awt.EventQueue.invokeLater(() -> {
			
			flmfr = new flamiumFire();
			flmfr.setVisible(true);
		});
		
		/* Create and display the form */
		java.awt.EventQueue.invokeLater(() -> {
			sbflm = new subflame();
			sbflm.setVisible(true);
		});
	}
	
	
	final public String _str_calibre = "clbr\n";
	final public String _str_irtest_ ="tstir\n";
	final public String _str_piezotest_ ="tstpzo";
	private String gstr = "";
	static subflame sbflm;
	static FlamiumGui flmg;
	static FlamiumMq flmmq;
	static FlamiumGraph flmgrp;
	static flamiumFire flmfr;
}
