using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class P1C : MonoBehaviour
{
    public Text P1CC;
    [SerializeField] GameObject Player;
    // Start is called before the first frame update
    void Start()
    {
        P1CC = GetComponent<Text>();
        Player = GameObject.Find("Player1");
    }

    // Update is called once per frame
    void Update()
    {
        P1CC.text = Player.GetComponent<Player1>().CoinCount.ToString();
    }
}
