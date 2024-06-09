using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class P2C : MonoBehaviour
{
    public Text P2CC;
    [SerializeField] GameObject Player;
    // Start is called before the first frame update
    void Start()
    {
        P2CC = GetComponent<Text>();
        Player = GameObject.Find("Player2");
    }

    // Update is called once per frame
    void Update()
    {
        P2CC.text = Player.GetComponent<Player2>().CoinCount.ToString();
    }
}
